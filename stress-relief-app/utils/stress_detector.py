"""
Age-aware stress detection module using EEG data analysis.

This module implements neuroscience-based stress detection using the Beta/(Alpha+Beta)
ratio (b_ab) from EEG signals. The Beta/(Alpha+Beta) ratio is a well-established
biomarker for cognitive stress and mental workload.

Neuroscience Background:
- Alpha waves (8-13 Hz): Associated with relaxed, calm states
- Beta waves (13-30 Hz): Associated with active thinking, focus, and stress
- Beta/(Alpha+Beta) ratio: Higher values indicate increased cognitive load and stress
  - Low ratio (<0.4): Calm, relaxed state
  - Medium ratio (0.4-0.6): Normal activity, mild stress
  - High ratio (>0.6): High stress, cognitive overload

Age-specific considerations:
- Children have naturally higher baseline beta activity
- Teens have variable stress responses during development
- Adults have more stable baseline patterns
- Thresholds are adjusted accordingly to account for developmental differences

Usage Example:
    detector = AgeAwareStressDetector(age_group='adult')
    
    # Calibrate baseline (collect 15 samples)
    for i in range(15):
        eeg_data = stream.get_latest_data()
        detector.calibrate_baseline(eeg_data)
        await asyncio.sleep(2)
    
    # Detect stress
    result = detector.detect_stress_level(eeg_data)
    print(f"Stress level: {result['level']} ({result['value']:.2f})")
    
    if detector.should_intervene():
        print("Intervention recommended")
"""

import numpy as np
from typing import Dict, List, Optional, Literal
from collections import deque
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class AgeAwareStressDetector:
    """
    Age-aware stress detector using EEG Beta/(Alpha+Beta) ratio.
    
    Implements personalized baseline calibration and age-specific thresholds
    for accurate stress detection across different age groups.
    """
    
    # Age-specific threshold configurations
    AGE_CONFIGS = {
        'child': {
            'stress_threshold': 0.45,      # Lower threshold for children
            'extreme_threshold': 0.65,     # Lower extreme threshold
            'intervention_delay': 10,      # 10 readings = 20 seconds (at 2Hz)
            'baseline_samples': 15,        # 15 samples for baseline (30 seconds)
            'min_age': 0,
            'max_age': 10
        },
        'teen': {
            'stress_threshold': 0.50,      # Moderate threshold for teens
            'extreme_threshold': 0.70,     # Moderate extreme threshold
            'intervention_delay': 15,      # 15 readings = 30 seconds
            'baseline_samples': 15,
            'min_age': 10,
            'max_age': 18
        },
        'adult': {
            'stress_threshold': 0.55,      # Higher threshold for adults
            'extreme_threshold': 0.75,     # Higher extreme threshold
            'intervention_delay': 20,      # 20 readings = 40 seconds
            'baseline_samples': 15,
            'min_age': 18,
            'max_age': 120
        }
    }
    
    # Stress level configurations
    STRESS_LEVELS = {
        'calm': {
            'emoji': '😌',
            'color': '#4CAF50',  # Green
            'message': 'Calm and relaxed'
        },
        'stressed': {
            'emoji': '😰',
            'color': '#FF9800',  # Orange
            'message': 'Elevated stress detected'
        },
        'extreme': {
            'emoji': '🚨',
            'color': '#F44336',  # Red
            'message': 'Extreme stress - intervention needed'
        },
        'unknown': {
            'emoji': '❓',
            'color': '#9E9E9E',  # Gray
            'message': 'Unable to determine stress level'
        }
    }
    
    def __init__(self, age_group: Literal['child', 'teen', 'adult'] = 'adult'):
        """
        Initialize the age-aware stress detector.
        
        Args:
            age_group: Age group category ('child', 'teen', or 'adult')
            
        Raises:
            ValueError: If age_group is not one of the valid options
        """
        if age_group not in self.AGE_CONFIGS:
            raise ValueError(f"Invalid age_group: {age_group}. Must be 'child', 'teen', or 'adult'")
        
        self.age_group = age_group
        self.config = self.AGE_CONFIGS[age_group]
        
        # Baseline calibration state
        self.baseline_calibrated = False
        self.baseline_samples: List[float] = []
        self.personal_baseline: Optional[float] = None
        self.baseline_std: Optional[float] = None
        
        # Adjusted thresholds (will be set after baseline calibration)
        self.stress_threshold = self.config['stress_threshold']
        self.extreme_threshold = self.config['extreme_threshold']
        
        # History tracking (last 60 readings = 2 minutes at 2Hz)
        self.history: deque = deque(maxlen=60)
        self.sustained_stress_count = 0
        self.extreme_stress_episodes = 0
        self.last_intervention_check = None
        
        logger.info(f"Initialized {age_group} stress detector with thresholds: "
                   f"stress={self.stress_threshold:.2f}, extreme={self.extreme_threshold:.2f}")
    
    def calibrate_baseline(self, data: Dict) -> bool:
        """
        Calibrate personal baseline from EEG data samples.
        
        Collects baseline samples and calculates personalized baseline and standard
        deviation. Adjusts thresholds relative to the personal baseline.
        
        Formula:
            personal_baseline = mean(b_ab_samples)
            baseline_std = std(b_ab_samples)
            adjusted_threshold = base_threshold + (personal_baseline - age_baseline_mean)
        
        Args:
            data: EEG data dictionary with 'Left__b_ab' and 'Right__b_ab' keys
            
        Returns:
            True if baseline calibration is complete, False if still collecting samples
        """
        if self.baseline_calibrated:
            logger.debug("Baseline already calibrated")
            return True
        
        # Extract b_ab ratio from data
        b_ab = self._extract_b_ab_ratio(data)
        if b_ab is None:
            logger.warning("Could not extract b_ab ratio from data")
            return False
        
        # Check signal quality - skip poor quality samples
        signal_quality = self._get_signal_quality(data)
        if signal_quality > 0.5:  # Skip if signal quality is poor (>50% bad)
            logger.debug(f"Skipping baseline sample due to poor signal quality: {signal_quality:.2f}")
            return False
        
        # Add sample to baseline collection
        self.baseline_samples.append(b_ab)
        logger.debug(f"Baseline sample {len(self.baseline_samples)}/{self.config['baseline_samples']}: {b_ab:.3f}")
        
        # Check if we have enough samples
        if len(self.baseline_samples) >= self.config['baseline_samples']:
            # Calculate personal baseline statistics
            samples_array = np.array(self.baseline_samples)
            self.personal_baseline = float(np.mean(samples_array))
            self.baseline_std = float(np.std(samples_array))
            
            # Adjust thresholds relative to personal baseline
            # If personal baseline is higher than expected, shift thresholds up
            # If personal baseline is lower, shift thresholds down
            baseline_offset = self.personal_baseline - 0.4  # 0.4 is typical baseline
            
            self.stress_threshold = self.config['stress_threshold'] + baseline_offset
            self.extreme_threshold = self.config['extreme_threshold'] + baseline_offset
            
            # Ensure thresholds stay within reasonable bounds
            self.stress_threshold = np.clip(self.stress_threshold, 0.3, 0.8)
            self.extreme_threshold = np.clip(self.extreme_threshold, 0.5, 0.9)
            
            self.baseline_calibrated = True
            
            logger.info(f"Baseline calibrated: {self.personal_baseline:.3f} ± {self.baseline_std:.3f}")
            logger.info(f"Adjusted thresholds: stress={self.stress_threshold:.3f}, "
                       f"extreme={self.extreme_threshold:.3f}")
            
            return True
        
        return False
    
    def detect_stress_level(self, data: Dict) -> Dict:
        """
        Detect stress level from EEG data.
        
        Uses the Beta/(Alpha+Beta) ratio as the primary stress indicator.
        The ratio is calculated as: beta / (alpha + beta)
        
        Higher ratios indicate:
        - Increased beta activity (active thinking, stress)
        - Decreased alpha activity (less relaxation)
        
        Args:
            data: EEG data dictionary with required keys:
                - 'Left__b_ab' or 'Right__b_ab': Beta/(Alpha+Beta) ratio
                - 'Left__p_bad' and 'Right__p_bad': Signal quality indicators
                - 'time': Timestamp (optional)
        
        Returns:
            Dictionary with stress detection results:
            {
                'level': 'calm' | 'stressed' | 'extreme' | 'unknown',
                'value': float,  # Current b_ab ratio
                'quality': float,  # Signal quality (0=good, 1=bad)
                'emoji': str,  # Emoji representation
                'color': str,  # Hex color code
                'message': str,  # Human-readable message
                'baseline': float,  # Personal baseline value
                'timestamp': float  # Unix timestamp
            }
        """
        # Extract b_ab ratio (average of left and right if available)
        b_ab = self._extract_b_ab_ratio(data)
        if b_ab is None:
            return self._create_result('unknown', 0.0, 1.0, "No valid b_ab data")
        
        # Get signal quality
        signal_quality = self._get_signal_quality(data)
        
        # If signal quality is too poor, return unknown
        if signal_quality > 0.7:  # More than 70% bad signal
            return self._create_result('unknown', b_ab, signal_quality, 
                                     "Poor signal quality - unable to detect stress")
        
        # Determine stress level based on thresholds
        # Use personal baseline-adjusted thresholds if calibrated, otherwise use age defaults
        stress_threshold = self.stress_threshold
        extreme_threshold = self.extreme_threshold
        
        if b_ab < stress_threshold:
            level = 'calm'
        elif b_ab < extreme_threshold:
            level = 'stressed'
        else:
            level = 'extreme'
        
        # Add to history
        timestamp = data.get('time', datetime.now().timestamp())
        self.history.append({
            'b_ab': b_ab,
            'level': level,
            'quality': signal_quality,
            'timestamp': timestamp
        })
        
        # Update sustained stress tracking
        self._update_stress_tracking(level)
        
        # Create result dictionary
        result = self._create_result(level, b_ab, signal_quality)
        result['baseline'] = self.personal_baseline if self.personal_baseline else 0.0
        result['timestamp'] = timestamp
        
        return result
    
    def should_intervene(self) -> bool:
        """
        Determine if stress intervention should be triggered.
        
        Intervention is recommended when:
        1. Stress level has been 'stressed' or 'extreme' for the configured delay period
        2. Signal quality is acceptable
        3. Baseline has been calibrated
        
        The intervention delay prevents false positives from brief stress spikes.
        
        Returns:
            True if intervention should be triggered, False otherwise
        """
        if not self.baseline_calibrated:
            logger.debug("Baseline not calibrated - intervention check skipped")
            return False
        
        if len(self.history) < self.config['intervention_delay']:
            return False
        
        # Check last N readings (where N = intervention_delay)
        recent_readings = list(self.history)[-self.config['intervention_delay']:]
        
        # Count how many are stressed or extreme
        stressed_count = sum(1 for r in recent_readings 
                           if r['level'] in ['stressed', 'extreme'] and r['quality'] < 0.7)
        
        # Require at least 80% of readings to be stressed/extreme
        threshold_ratio = 0.8
        required_count = int(self.config['intervention_delay'] * threshold_ratio)
        
        should_intervene = stressed_count >= required_count
        
        if should_intervene:
            logger.info(f"Intervention recommended: {stressed_count}/{self.config['intervention_delay']} "
                       f"recent readings show stress")
        
        return should_intervene
    
    def needs_crisis_intervention(self) -> bool:
        """
        Determine if immediate crisis intervention is needed.
        
        Crisis intervention is triggered when:
        1. Current or recent readings show 'extreme' stress
        2. Signal quality is acceptable
        3. Baseline has been calibrated
        
        This is more urgent than regular intervention and should trigger
        immediate action.
        
        Returns:
            True if crisis intervention is needed, False otherwise
        """
        if not self.baseline_calibrated:
            return False
        
        if len(self.history) == 0:
            return False
        
        # Check last few readings for extreme stress
        # Use shorter window for crisis detection (last 5 readings = 10 seconds)
        recent_readings = list(self.history)[-5:]
        
        # Check if any recent reading shows extreme stress with good signal
        for reading in recent_readings:
            if reading['level'] == 'extreme' and reading['quality'] < 0.7:
                logger.warning("Crisis intervention needed: extreme stress detected")
                return True
        
        return False
    
    def _extract_b_ab_ratio(self, data: Dict) -> Optional[float]:
        """
        Extract Beta/(Alpha+Beta) ratio from EEG data.
        
        Uses average of left and right channels if both available,
        otherwise uses whichever is available.
        
        Args:
            data: EEG data dictionary
            
        Returns:
            b_ab ratio as float, or None if not available
        """
        left_b_ab = data.get('Left__b_ab')
        right_b_ab = data.get('Right__b_ab')
        
        if left_b_ab is not None and right_b_ab is not None:
            # Average of left and right for more robust measurement
            return (float(left_b_ab) + float(right_b_ab)) / 2.0
        elif left_b_ab is not None:
            return float(left_b_ab)
        elif right_b_ab is not None:
            return float(right_b_ab)
        else:
            return None
    
    def _get_signal_quality(self, data: Dict) -> float:
        """
        Get overall signal quality from p_bad values.
        
        p_bad represents the proportion of bad signal (0=good, 1=bad).
        We average left and right channels for overall quality assessment.
        
        Args:
            data: EEG data dictionary with 'Left__p_bad' and 'Right__p_bad'
            
        Returns:
            Average signal quality (0=good, 1=bad)
        """
        left_p_bad = data.get('Left__p_bad', 0.5)  # Default to moderate if missing
        right_p_bad = data.get('Right__p_bad', 0.5)
        
        return (float(left_p_bad) + float(right_p_bad)) / 2.0
    
    def _create_result(
        self, 
        level: Literal['calm', 'stressed', 'extreme', 'unknown'],
        value: float,
        quality: float,
        custom_message: Optional[str] = None
    ) -> Dict:
        """
        Create a standardized result dictionary.
        
        Args:
            level: Stress level category
            value: Current b_ab ratio value
            quality: Signal quality (0=good, 1=bad)
            custom_message: Optional custom message (overrides default)
            
        Returns:
            Result dictionary with all required fields
        """
        level_config = self.STRESS_LEVELS[level]
        
        message = custom_message if custom_message else level_config['message']
        
        # Add quality warning if signal is poor
        if quality > 0.5:
            message += f" (Signal quality: {quality:.1%})"
        
        return {
            'level': level,
            'value': value,
            'quality': quality,
            'emoji': level_config['emoji'],
            'color': level_config['color'],
            'message': message,
            'baseline': self.personal_baseline if self.personal_baseline else 0.0
        }
    
    def _update_stress_tracking(self, level: str) -> None:
        """
        Update internal stress tracking statistics.
        
        Tracks sustained stress duration and counts extreme stress episodes.
        
        Args:
            level: Current stress level
        """
        # Update sustained stress count
        if level in ['stressed', 'extreme']:
            self.sustained_stress_count += 1
        else:
            self.sustained_stress_count = 0
        
        # Track extreme stress episodes
        if level == 'extreme':
            # Check if this is a new episode (previous reading wasn't extreme)
            if len(self.history) > 1:
                prev_level = list(self.history)[-2]['level']
                if prev_level != 'extreme':
                    self.extreme_stress_episodes += 1
                    logger.warning(f"Extreme stress episode #{self.extreme_stress_episodes} detected")
        else:
            # Reset count if we have a gap (not consecutive)
            pass
    
    def get_stress_statistics(self) -> Dict:
        """
        Get comprehensive stress statistics from history.
        
        Returns:
            Dictionary with statistics:
            {
                'total_readings': int,
                'calm_percentage': float,
                'stressed_percentage': float,
                'extreme_percentage': float,
                'sustained_stress_duration': int,  # readings
                'extreme_episodes': int,
                'average_b_ab': float,
                'baseline_calibrated': bool
            }
        """
        if len(self.history) == 0:
            return {
                'total_readings': 0,
                'calm_percentage': 0.0,
                'stressed_percentage': 0.0,
                'extreme_percentage': 0.0,
                'sustained_stress_duration': 0,
                'extreme_episodes': self.extreme_stress_episodes,
                'average_b_ab': 0.0,
                'baseline_calibrated': self.baseline_calibrated
            }
        
        total = len(self.history)
        calm_count = sum(1 for r in self.history if r['level'] == 'calm')
        stressed_count = sum(1 for r in self.history if r['level'] == 'stressed')
        extreme_count = sum(1 for r in self.history if r['level'] == 'extreme')
        
        b_ab_values = [r['b_ab'] for r in self.history]
        avg_b_ab = float(np.mean(b_ab_values))
        
        return {
            'total_readings': total,
            'calm_percentage': (calm_count / total) * 100,
            'stressed_percentage': (stressed_count / total) * 100,
            'extreme_percentage': (extreme_count / total) * 100,
            'sustained_stress_duration': self.sustained_stress_count,
            'extreme_episodes': self.extreme_stress_episodes,
            'average_b_ab': avg_b_ab,
            'baseline_calibrated': self.baseline_calibrated
        }
    
    def reset_calibration(self) -> None:
        """Reset baseline calibration and clear history."""
        self.baseline_calibrated = False
        self.baseline_samples.clear()
        self.personal_baseline = None
        self.baseline_std = None
        self.stress_threshold = self.config['stress_threshold']
        self.extreme_threshold = self.config['extreme_threshold']
        self.history.clear()
        self.sustained_stress_count = 0
        self.extreme_stress_episodes = 0
        logger.info("Calibration and history reset")


# Example usage and testing

if __name__ == "__main__":
    # Example: Adult stress detector
    detector = AgeAwareStressDetector(age_group='adult')
    
    # Simulate baseline calibration
    print("Calibrating baseline...")
    for i in range(15):
        mock_data = {
            'Left__b_ab': 0.35 + np.random.normal(0, 0.05),
            'Right__b_ab': 0.35 + np.random.normal(0, 0.05),
            'Left__p_bad': 0.1,
            'Right__p_bad': 0.1,
            'time': datetime.now().timestamp()
        }
        detector.calibrate_baseline(mock_data)
    
    # Simulate stress detection
    print("\nDetecting stress levels...")
    for i in range(10):
        # Simulate increasing stress
        stress_value = 0.4 + (i * 0.05)
        mock_data = {
            'Left__b_ab': stress_value,
            'Right__b_ab': stress_value,
            'Left__p_bad': 0.1,
            'Right__p_bad': 0.1,
            'time': datetime.now().timestamp()
        }
        
        result = detector.detect_stress_level(mock_data)
        print(f"Reading {i+1}: {result['emoji']} {result['level']:8s} "
              f"(b_ab={result['value']:.3f}, baseline={result['baseline']:.3f})")
    
    # Check intervention status
    print(f"\nShould intervene: {detector.should_intervene()}")
    print(f"Needs crisis intervention: {detector.needs_crisis_intervention()}")
    
    # Get statistics
    stats = detector.get_stress_statistics()
    print(f"\nStatistics: {stats}")
