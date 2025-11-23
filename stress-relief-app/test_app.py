#!/usr/bin/env python3
"""
Quick test script to verify app structure and imports.
This doesn't run Streamlit, just checks if everything is set up correctly.
"""

import sys
import os

def test_imports():
    """Test if all modules can be imported."""
    print("Testing imports...")
    
    # Add current directory to path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    errors = []
    
    # Test core dependencies
    try:
        import streamlit
        print("  ✓ streamlit")
    except ImportError as e:
        errors.append(f"streamlit: {e}")
        print(f"  ✗ streamlit: {e}")
    
    try:
        import plotly
        print("  ✓ plotly")
    except ImportError as e:
        errors.append(f"plotly: {e}")
        print(f"  ✗ plotly: {e}")
    
    try:
        import pandas
        print("  ✓ pandas")
    except ImportError as e:
        errors.append(f"pandas: {e}")
        print(f"  ✗ pandas: {e}")
    
    try:
        import numpy
        print("  ✓ numpy")
    except ImportError as e:
        errors.append(f"numpy: {e}")
        print(f"  ✗ numpy: {e}")
    
    try:
        import websockets
        print("  ✓ websockets")
    except ImportError as e:
        errors.append(f"websockets: {e}")
        print(f"  ✗ websockets: {e}")
    
    # Test utility modules (may fail if dependencies missing, but syntax should be OK)
    print("\nTesting utility modules...")
    
    try:
        from utils.stress_detector import AgeAwareStressDetector
        print("  ✓ stress_detector")
    except Exception as e:
        print(f"  ⚠ stress_detector: {e} (may need dependencies)")
    
    try:
        from utils.neurable_stream import NeurableStream
        print("  ✓ neurable_stream")
    except Exception as e:
        print(f"  ⚠ neurable_stream: {e} (may need dependencies)")
    
    try:
        from utils.ai_helper import AIHelper
        print("  ✓ ai_helper")
    except Exception as e:
        print(f"  ⚠ ai_helper: {e} (may need dependencies)")
    
    try:
        from utils.db_helper import DBHelper
        print("  ✓ db_helper")
    except Exception as e:
        print(f"  ⚠ db_helper: {e} (may need dependencies)")
    
    try:
        from components.interventions import InterventionManager
        print("  ✓ interventions")
    except Exception as e:
        print(f"  ⚠ interventions: {e} (may need dependencies)")
    
    try:
        from components.visualizations import VisualizationManager
        print("  ✓ visualizations")
    except Exception as e:
        print(f"  ⚠ visualizations: {e} (may need dependencies)")
    
    return errors

def test_file_structure():
    """Test if all required files exist."""
    print("\nTesting file structure...")
    
    required_files = [
        'app.py',
        'requirements.txt',
        '.env.example',
        'utils/__init__.py',
        'utils/stress_detector.py',
        'utils/ai_helper.py',
        'utils/db_helper.py',
        'utils/neurable_stream.py',
        'components/__init__.py',
        'components/interventions.py',
        'components/visualizations.py',
        'data/stories.json'
    ]
    
    missing = []
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✓ {file}")
        else:
            missing.append(file)
            print(f"  ✗ {file} (missing)")
    
    return missing

def main():
    """Run all tests."""
    print("=" * 50)
    print("Stress Relief Companion - App Test")
    print("=" * 50)
    print()
    
    # Test file structure
    missing_files = test_file_structure()
    
    # Test imports
    import_errors = test_imports()
    
    # Summary
    print("\n" + "=" * 50)
    print("Test Summary")
    print("=" * 50)
    
    if missing_files:
        print(f"⚠ Missing files: {len(missing_files)}")
        for file in missing_files:
            print(f"  - {file}")
    else:
        print("✓ All required files present")
    
    if import_errors:
        print(f"\n⚠ Import errors: {len(import_errors)}")
        print("  Install dependencies: pip install -r requirements.txt")
        for error in import_errors:
            print(f"  - {error}")
    else:
        print("\n✓ All core dependencies available")
    
    print("\n" + "=" * 50)
    
    if missing_files or import_errors:
        print("\n⚠ Some issues found. Run setup.sh to install dependencies.")
        return 1
    else:
        print("\n✅ App structure looks good! You can run: streamlit run app.py")
        return 0

if __name__ == "__main__":
    sys.exit(main())

