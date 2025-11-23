"""
Neurable EEG data streaming module.

This module provides a clean interface for connecting to and receiving real-time
EEG data from Neurable headsets via WebSocket.

Usage Examples:
    # Real hardware connection
    stream = NeurableStream(websocket_url="ws://localhost:8080")
    await stream.connect()
    
    if stream.is_connected():
        data = stream.get_latest_data()
        print(f"Stress level: {data['Left__b_ab']}")
    
    await stream.disconnect()
    
    # Test mode with simulated data
    stream = NeurableStream(test_mode=True, stress_level="calm")
    await stream.connect()
    
    # In a loop or async context
    data = stream.get_latest_data()
    
    await stream.disconnect()
"""

import asyncio
import json
import logging
import random
import ssl
import time
from typing import Dict, Optional, Literal
import websockets
from websockets.exceptions import ConnectionClosed, InvalidURI, InvalidState

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NeurableStream:
    """
    Handles real-time EEG data streaming from Neurable devices.
    
    Provides a clean interface for connecting to Neurable headsets, receiving
    EEG data, and includes a test mode for development without hardware.
    """
    
    # Expected data format keys
    REQUIRED_KEYS = [
        'Left__b_ab', 'Right__b_ab',
        'Left__alpha', 'Right__alpha',
        'Left__beta', 'Right__beta',
        'Left__theta', 'Right__theta',
        'Left__p_bad', 'Right__p_bad',
        'time'
    ]
    
    def __init__(
        self,
        websocket_url: Optional[str] = None,
        test_mode: bool = False,
        stress_level: Literal["calm", "stressed", "extreme"] = "calm",
        connection_timeout: float = 10.0,
        receive_timeout: float = 5.0
    ):
        """
        Initialize the NeurableStream.
        
        Args:
            websocket_url: WebSocket URL for EEG data stream (e.g., "ws://localhost:8080")
            test_mode: If True, generates mock data instead of connecting to hardware
            stress_level: Stress level for test mode ("calm", "stressed", "extreme")
            connection_timeout: Timeout for WebSocket connection in seconds
            receive_timeout: Timeout for receiving data in seconds
            
        Raises:
            ValueError: If websocket_url is None and test_mode is False
        """
        if not test_mode and not websocket_url:
            raise ValueError("websocket_url must be provided when test_mode is False")
        
        self.websocket_url = websocket_url
        self.test_mode = test_mode
        self.stress_level = stress_level
        self.connection_timeout = connection_timeout
        self.receive_timeout = receive_timeout
        
        # Connection state
        self._websocket: Optional[websockets.WebSocketClientProtocol] = None
        self._connected = False
        self._running = False
        self._latest_data: Optional[Dict] = None
        self._data_lock = asyncio.Lock()
        
        # Background task for receiving data
        self._receive_task: Optional[asyncio.Task] = None
        self._mock_task: Optional[asyncio.Task] = None
        
        # Error tracking
        self._last_error: Optional[str] = None
    
    async def connect(self) -> bool:
        """
        Connect to the Neurable EEG data stream.
        
        Returns:
            True if connection successful, False otherwise
            
        Example:
            success = await stream.connect()
            if success:
                print("Connected successfully")
        """
        if self._connected:
            logger.warning("Already connected. Disconnect first before reconnecting.")
            return True
        
        try:
            if self.test_mode:
                return await self._start_test_mode()
            else:
                return await self._connect_to_websocket()
        except Exception as e:
            logger.error(f"Connection error: {str(e)}")
            self._last_error = str(e)
            self._connected = False
            return False
    
    async def _connect_to_websocket(self) -> bool:
        """Establish WebSocket connection to Neurable headset."""
        try:
            logger.info(f"Connecting to {self.websocket_url}...")
            
            # Check if using secure WebSocket (wss://)
            use_ssl = self.websocket_url.startswith('wss://')
            ssl_context = None
            
            if use_ssl:
                # Create SSL context (disable certificate verification for testing)
                ssl_context = ssl.create_default_context()
                ssl_context.check_hostname = False
                ssl_context.verify_mode = ssl.CERT_NONE
                logger.info("Using SSL connection (certificate verification disabled)")
            
            self._websocket = await asyncio.wait_for(
                websockets.connect(
                    self.websocket_url,
                    ssl=ssl_context,
                    ping_interval=20,
                    ping_timeout=10
                ),
                timeout=self.connection_timeout
            )
            
            self._connected = True
            self._running = True
            self._receive_task = asyncio.create_task(self._receive_data_loop())
            
            logger.info("Successfully connected to Neurable stream")
            return True
            
        except asyncio.TimeoutError:
            error_msg = f"Connection timeout after {self.connection_timeout}s"
            logger.error(error_msg)
            self._last_error = error_msg
            return False
            
        except InvalidURI as e:
            error_msg = f"Invalid WebSocket URL: {str(e)}"
            logger.error(error_msg)
            self._last_error = error_msg
            return False
            
        except ConnectionRefusedError:
            error_msg = "Connection refused. Is the Neurable stream server running?"
            logger.error(error_msg)
            self._last_error = error_msg
            return False
            
        except Exception as e:
            error_msg = f"Unexpected connection error: {str(e)}"
            logger.error(error_msg)
            self._last_error = error_msg
            return False
    
    async def _receive_data_loop(self) -> None:
        """Continuously receive and process data from WebSocket."""
        while self._running and self._connected:
            try:
                # Receive message with timeout
                message = await asyncio.wait_for(
                    self._websocket.recv(),
                    timeout=self.receive_timeout
                )
                
                # Parse JSON data
                try:
                    raw_data = json.loads(message)
                    processed_data = self._process_data(raw_data)
                    
                    async with self._data_lock:
                        self._latest_data = processed_data
                        self._last_error = None
                        
                except json.JSONDecodeError as e:
                    error_msg = f"JSON decode error: {str(e)}"
                    logger.warning(error_msg)
                    self._last_error = error_msg
                    continue
                    
                except ValueError as e:
                    error_msg = f"Data validation error: {str(e)}"
                    logger.warning(error_msg)
                    self._last_error = error_msg
                    continue
                    
            except asyncio.TimeoutError:
                # Timeout is not necessarily an error - just no new data
                logger.debug("No data received within timeout period")
                continue
                
            except ConnectionClosed:
                error_msg = "WebSocket connection closed"
                logger.warning(error_msg)
                self._last_error = error_msg
                self._connected = False
                self._running = False
                break
                
            except Exception as e:
                error_msg = f"Error receiving data: {str(e)}"
                logger.error(error_msg)
                self._last_error = error_msg
                await asyncio.sleep(1)  # Brief pause before retrying
    
    def _process_data(self, raw_data: Dict) -> Dict:
        """
        Process and validate raw EEG data.
        
        Handles variations in data format from the stream.
        
        Args:
            raw_data: Raw data dictionary from stream
            
        Returns:
            Processed and validated data dictionary
            
        Raises:
            ValueError: If required keys are missing or data is invalid
        """
        processed = {}
        
        # Process frequency band ratios (b_ab) - required
        for key in ['Left__b_ab', 'Right__b_ab']:
            if key not in raw_data:
                # Try alternative naming
                alt_key = key.replace('__', '_')
                if alt_key in raw_data:
                    processed[key] = float(raw_data[alt_key])
                else:
                    raise ValueError(f"Missing required key: {key}")
            else:
                value = float(raw_data[key])
                if not 0 <= value <= 1:
                    logger.warning(f"{key} out of expected range [0, 1]: {value}")
                processed[key] = value
        
        # Process frequency bands - try to get all, but make some optional
        for key in ['Left__alpha', 'Right__alpha', 'Left__beta', 'Right__beta',
                   'Left__theta', 'Right__theta']:
            if key in raw_data:
                value = float(raw_data[key])
                if value < 0:
                    logger.warning(f"{key} is negative: {value}")
                processed[key] = value
            else:
                # Use default value if missing
                processed[key] = 0.0
                logger.debug(f"Missing optional key {key}, using default 0.0")
        
        # Process signal quality (p_bad) - try to get, use defaults if missing
        for key in ['Left__p_bad', 'Right__p_bad']:
            if key in raw_data:
                value = float(raw_data[key])
                if not 0 <= value <= 1:
                    logger.warning(f"{key} out of expected range [0, 1]: {value}")
                processed[key] = value
            else:
                # Use default good signal quality if missing
                processed[key] = 0.0
                logger.debug(f"Missing signal quality {key}, assuming good signal")
        
        # Process timestamp - use current time if missing
        if 'time' in raw_data:
            processed['time'] = float(raw_data['time'])
        else:
            processed['time'] = time.time()
            logger.debug("Missing timestamp, using current time")
        
        return processed
    
    async def _start_test_mode(self) -> bool:
        """Start test mode with mock data generation."""
        logger.info(f"Starting test mode with stress level: {self.stress_level}")
        self._connected = True
        self._running = True
        self._mock_task = asyncio.create_task(self._generate_mock_data())
        return True
    
    async def _generate_mock_data(self) -> None:
        """Generate mock EEG data based on stress level."""
        while self._running:
            try:
                mock_data = self._create_mock_data()
                
                async with self._data_lock:
                    self._latest_data = mock_data
                
                # Simulate data rate (e.g., 10 Hz)
                await asyncio.sleep(0.1)
                
            except Exception as e:
                logger.error(f"Error generating mock data: {str(e)}")
                await asyncio.sleep(1)
    
    def _create_mock_data(self) -> Dict:
        """
        Create mock EEG data based on current stress level.
        
        Returns:
            Dictionary with mock EEG data matching the expected format
        """
        base_time = time.time()
        
        if self.stress_level == "calm":
            # Calm state: low beta, high alpha, good signal quality
            return {
                'Left__b_ab': random.uniform(0.2, 0.35),  # Low beta/(alpha+beta)
                'Right__b_ab': random.uniform(0.2, 0.35),
                'Left__alpha': random.uniform(0.4, 0.6),  # High alpha
                'Right__alpha': random.uniform(0.4, 0.6),
                'Left__beta': random.uniform(0.15, 0.25),  # Low beta
                'Right__beta': random.uniform(0.15, 0.25),
                'Left__theta': random.uniform(0.1, 0.2),
                'Right__theta': random.uniform(0.1, 0.2),
                'Left__p_bad': random.uniform(0.0, 0.1),  # Good signal
                'Right__p_bad': random.uniform(0.0, 0.1),
                'time': base_time
            }
            
        elif self.stress_level == "stressed":
            # Stressed state: high beta, low alpha, moderate signal quality
            return {
                'Left__b_ab': random.uniform(0.5, 0.7),  # High beta/(alpha+beta)
                'Right__b_ab': random.uniform(0.5, 0.7),
                'Left__alpha': random.uniform(0.2, 0.35),  # Low alpha
                'Right__alpha': random.uniform(0.2, 0.35),
                'Left__beta': random.uniform(0.4, 0.6),  # High beta
                'Right__beta': random.uniform(0.4, 0.6),
                'Left__theta': random.uniform(0.15, 0.25),
                'Right__theta': random.uniform(0.15, 0.25),
                'Left__p_bad': random.uniform(0.2, 0.4),  # Moderate signal
                'Right__p_bad': random.uniform(0.2, 0.4),
                'time': base_time
            }
            
        else:  # extreme
            # Extreme stress: very high beta, very low alpha, poor signal quality
            return {
                'Left__b_ab': random.uniform(0.7, 0.9),  # Very high beta/(alpha+beta)
                'Right__b_ab': random.uniform(0.7, 0.9),
                'Left__alpha': random.uniform(0.1, 0.2),  # Very low alpha
                'Right__alpha': random.uniform(0.1, 0.2),
                'Left__beta': random.uniform(0.6, 0.8),  # Very high beta
                'Right__beta': random.uniform(0.6, 0.8),
                'Left__theta': random.uniform(0.2, 0.3),
                'Right__theta': random.uniform(0.2, 0.3),
                'Left__p_bad': random.uniform(0.5, 0.8),  # Poor signal
                'Right__p_bad': random.uniform(0.5, 0.8),
                'time': base_time
            }
    
    def get_latest_data(self) -> Optional[Dict]:
        """
        Get the latest received EEG data.
        
        Returns:
            Dictionary with EEG data in the expected format, or None if no data available
            
        Example:
            data = stream.get_latest_data()
            if data:
                stress_ratio = data['Left__b_ab']
                signal_quality = data['Left__p_bad']
        """
        # Note: This is not async, but we need to access the lock
        # In a real async context, you might want to make this async
        if not self._connected:
            return None
        
        # For thread-safe access in sync context
        # In production, consider using asyncio.run() or making this async
        try:
            if self._latest_data:
                # Return a copy to prevent external modification
                return self._latest_data.copy()
        except Exception as e:
            logger.error(f"Error getting latest data: {str(e)}")
        
        return None
    
    async def get_latest_data_async(self) -> Optional[Dict]:
        """
        Async version of get_latest_data() for proper async/await usage.
        
        Returns:
            Dictionary with EEG data or None if no data available
        """
        if not self._connected:
            return None
        
        async with self._data_lock:
            if self._latest_data:
                return self._latest_data.copy()
        
        return None
    
    def is_connected(self) -> bool:
        """
        Check if currently connected to the stream.
        
        Returns:
            True if connected, False otherwise
            
        Example:
            if stream.is_connected():
                data = stream.get_latest_data()
        """
        return self._connected
    
    def get_last_error(self) -> Optional[str]:
        """
        Get the last error message, if any.
        
        Returns:
            Error message string or None if no errors
        """
        return self._last_error
    
    async def disconnect(self) -> None:
        """
        Disconnect from the EEG stream and clean up resources.
        
        Example:
            await stream.disconnect()
        """
        if not self._connected:
            logger.info("Not connected, nothing to disconnect")
            return
        
        logger.info("Disconnecting from Neurable stream...")
        self._running = False
        self._connected = False
        
        # Cancel background tasks
        if self._receive_task and not self._receive_task.done():
            self._receive_task.cancel()
            try:
                await self._receive_task
            except asyncio.CancelledError:
                pass
        
        if self._mock_task and not self._mock_task.done():
            self._mock_task.cancel()
            try:
                await self._mock_task
            except asyncio.CancelledError:
                pass
        
        # Close WebSocket connection
        if self._websocket:
            try:
                await self._websocket.close()
            except Exception as e:
                logger.warning(f"Error closing WebSocket: {str(e)}")
            finally:
                self._websocket = None
        
        # Clear latest data
        async with self._data_lock:
            self._latest_data = None
        
        logger.info("Disconnected successfully")
    
    async def __aenter__(self):
        """Async context manager entry."""
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.disconnect()


# Example usage functions

async def example_real_connection():
    """Example: Connect to real Neurable hardware."""
    stream = NeurableStream(websocket_url="ws://localhost:8080")
    
    try:
        if await stream.connect():
            print("Connected!")
            
            # Get data in a loop
            for _ in range(10):
                data = await stream.get_latest_data_async()
                if data:
                    print(f"Beta/(Alpha+Beta) ratio: {data['Left__b_ab']:.3f}")
                    print(f"Signal quality (Left): {data['Left__p_bad']:.3f}")
                await asyncio.sleep(1)
        else:
            print(f"Connection failed: {stream.get_last_error()}")
            
    finally:
        await stream.disconnect()


async def example_test_mode():
    """Example: Use test mode with simulated data."""
    # Test calm state
    stream = NeurableStream(test_mode=True, stress_level="calm")
    
    try:
        await stream.connect()
        print("Test mode connected (calm state)")
        
        for _ in range(5):
            data = await stream.get_latest_data_async()
            if data:
                print(f"Calm - Beta/(Alpha+Beta): {data['Left__b_ab']:.3f}")
            await asyncio.sleep(0.5)
        
    finally:
        await stream.disconnect()
    
    # Test stressed state
    stream = NeurableStream(test_mode=True, stress_level="stressed")
    
    try:
        await stream.connect()
        print("\nTest mode connected (stressed state)")
        
        for _ in range(5):
            data = await stream.get_latest_data_async()
            if data:
                print(f"Stressed - Beta/(Alpha+Beta): {data['Left__b_ab']:.3f}")
            await asyncio.sleep(0.5)
            
    finally:
        await stream.disconnect()


async def example_context_manager():
    """Example: Use as async context manager."""
    async with NeurableStream(test_mode=True, stress_level="calm") as stream:
        if stream.is_connected():
            data = await stream.get_latest_data_async()
            if data:
                print(f"Data received: {data['Left__b_ab']}")


if __name__ == "__main__":
    # Run test mode example
    asyncio.run(example_test_mode())
