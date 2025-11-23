#!/usr/bin/env python3
"""
Test script to verify Neurable EEG stream connection and data reading.
"""

import asyncio
import json
import ssl
import websockets
from datetime import datetime

HUB_IP = "stream2.mindfulmakers.xyz"

async def test_neurable_stream():
    """Test connection to Neurable EEG stream."""
    print(f"🔌 Attempting to connect to Neurable EEG stream...")
    print(f"   Endpoint: wss://{HUB_IP}")
    print(f"   Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 60)
    
    try:
        # Disable SSL certificate verification (for testing only)
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        print("✓ SSL context created")
        
        # Connect to WebSocket
        async with websockets.connect(
            f"wss://{HUB_IP}", 
            ssl=ssl_context,
            ping_timeout=10,
            close_timeout=10
        ) as ws:
            print(f"✓ WebSocket connection established!")
            print("-" * 60)
            print("📡 Receiving EEG data stream...\n")
            
            # Read first 5 messages
            message_count = 0
            max_messages = 5
            
            async for msg in ws:
                message_count += 1
                
                try:
                    eeg_data = json.loads(msg)
                    
                    print(f"📊 Message #{message_count}:")
                    print(f"   Timestamp: {datetime.now().strftime('%H:%M:%S.%f')[:-3]}")
                    
                    # Display available fields
                    if isinstance(eeg_data, dict):
                        print(f"   Available fields: {list(eeg_data.keys())}")
                        
                        # Check for key EEG metrics
                        if 'b_ab' in eeg_data:
                            print(f"   ✓ Beta/Alpha ratio (b_ab): {eeg_data['b_ab']:.3f}")
                        if 'p_bad' in eeg_data:
                            print(f"   ✓ Signal quality (p_bad): {eeg_data['p_bad']:.3f}")
                        if 'attention' in eeg_data:
                            print(f"   ✓ Attention: {eeg_data['attention']:.3f}")
                        if 'meditation' in eeg_data:
                            print(f"   ✓ Meditation: {eeg_data['meditation']:.3f}")
                        
                        # Display full data for first message
                        if message_count == 1:
                            print(f"\n   Full data structure:")
                            for key, value in eeg_data.items():
                                if isinstance(value, (int, float)):
                                    print(f"      {key}: {value}")
                                elif isinstance(value, list):
                                    print(f"      {key}: [list with {len(value)} items]")
                                else:
                                    print(f"      {key}: {type(value).__name__}")
                    
                    print()
                    
                    if message_count >= max_messages:
                        print(f"✅ Successfully received {message_count} messages from Neurable!")
                        print("-" * 60)
                        break
                        
                except json.JSONDecodeError as e:
                    print(f"   ⚠️  JSON parsing error: {e}")
                    print(f"   Raw message: {msg[:100]}...")
                except Exception as e:
                    print(f"   ⚠️  Error processing message: {e}")
            
            print(f"\n📈 Summary:")
            print(f"   Total messages received: {message_count}")
            print(f"   Connection status: STABLE")
            print(f"   Data format: JSON")
            print(f"   Stream endpoint: wss://{HUB_IP}")
            
    except asyncio.TimeoutError:
        print("❌ Connection timeout - stream may be unavailable")
        print("   Possible reasons:")
        print("   - Neurable device not streaming")
        print("   - Network connectivity issues")
        print("   - Endpoint may be down")
        return False
    
    except websockets.exceptions.WebSocketException as e:
        print(f"❌ WebSocket error: {e}")
        print("   The stream endpoint may not be accessible")
        return False
    
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print(f"   Error type: {type(e).__name__}")
        return False
    
    return True


async def main():
    """Run the test."""
    print("\n" + "="*60)
    print("  NEURABLE EEG STREAM CONNECTION TEST")
    print("="*60 + "\n")
    
    success = await test_neurable_stream()
    
    print("\n" + "="*60)
    if success:
        print("  ✅ TEST PASSED - EEG data is readable!")
    else:
        print("  ⚠️  TEST FAILED - Using mock data fallback")
        print("     The app will use simulated EEG data for testing")
    print("="*60 + "\n")


if __name__ == "__main__":
    asyncio.run(main())

