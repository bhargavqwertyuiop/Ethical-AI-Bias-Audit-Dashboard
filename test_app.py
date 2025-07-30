#!/usr/bin/env python3
"""
Simple test script to verify the Ethical AI Bias Audit Dashboard works correctly.
This script tests basic functionality and imports.
"""

import sys
import importlib
import traceback

def test_imports():
    """Test that all required modules can be imported."""
    print("🧪 Testing imports...")
    
    modules_to_test = [
        'streamlit',
        'pandas',
        'numpy',
        'plotly.express',
        'plotly.graph_objects',
        'src.bias_detector',
        'src.mitigation_engine',
        'src.explainable_ai'
    ]
    
    failed_imports = []
    
    for module in modules_to_test:
        try:
            importlib.import_module(module)
            print(f"  ✅ {module}")
        except ImportError as e:
            print(f"  ❌ {module}: {e}")
            failed_imports.append(module)
        except Exception as e:
            print(f"  ⚠️  {module}: {e}")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"\n❌ Failed to import: {', '.join(failed_imports)}")
        return False
    else:
        print("\n✅ All imports successful!")
        return True

def test_bias_detector():
    """Test basic BiasDetector functionality."""
    print("\n🧪 Testing BiasDetector...")
    
    try:
        from src.bias_detector import BiasDetector
        import pandas as pd
        import numpy as np
        
        # Create sample data
        np.random.seed(42)
        data = pd.DataFrame({
            'feature1': np.random.normal(0, 1, 100),
            'feature2': np.random.normal(0, 1, 100),
            'gender': np.random.choice(['Male', 'Female'], 100),
            'outcome': np.random.choice([0, 1], 100)
        })
        
        # Initialize detector
        detector = BiasDetector()
        
        # Test bias detection
        results = detector.detect_dataset_bias(
            data=data,
            protected_attributes=['gender'],
            target_column='outcome'
        )
        
        print("  ✅ BiasDetector working correctly")
        return True
        
    except Exception as e:
        print(f"  ❌ BiasDetector test failed: {e}")
        traceback.print_exc()
        return False

def test_sample_data():
    """Test loading sample data."""
    print("\n🧪 Testing sample data loading...")
    
    try:
        import pandas as pd
        
        # Test loading sample data
        sample_data = pd.read_csv('data/sample_hiring_data.csv')
        
        print(f"  ✅ Sample data loaded: {len(sample_data)} rows, {len(sample_data.columns)} columns")
        
        # Check required columns
        required_columns = ['gender', 'race', 'hired']
        missing_columns = [col for col in required_columns if col not in sample_data.columns]
        
        if missing_columns:
            print(f"  ⚠️  Missing columns: {missing_columns}")
            return False
        else:
            print("  ✅ All required columns present")
            return True
            
    except Exception as e:
        print(f"  ❌ Sample data test failed: {e}")
        return False

def test_streamlit_compatibility():
    """Test Streamlit version compatibility."""
    print("\n🧪 Testing Streamlit compatibility...")
    
    try:
        import streamlit as st
        
        # Check if st.rerun is available (should be in v1.27.0+)
        if hasattr(st, 'rerun'):
            print("  ✅ st.rerun() is available")
        else:
            print("  ❌ st.rerun() is not available - please update Streamlit")
            return False
        
        # Check version
        if hasattr(st, '__version__'):
            print(f"  ✅ Streamlit version: {st.__version__}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Streamlit compatibility test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🛡️  Ethical AI Bias Audit Dashboard - Test Suite")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_streamlit_compatibility,
        test_sample_data,
        test_bias_detector
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"  💥 Test crashed: {e}")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The application should work correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())