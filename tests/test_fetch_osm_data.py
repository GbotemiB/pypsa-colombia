#!/usr/bin/env python3
"""
Test script to validate the fetch_osm_data functionality
"""

import sys
import os
from pathlib import Path

# Add the scripts directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

def test_fetch_osm_data_import():
    """Test that we can import the fetch_osm_data module"""
    try:
        from fetch_osm_data import setup_logging, country_list_to_geofk
        print("✓ Successfully imported fetch_osm_data functions")
        return True
    except ImportError as e:
        print(f"✗ Failed to import fetch_osm_data: {e}")
        return False

def test_country_mapping():
    """Test the country code to geofk mapping"""
    try:
        from fetch_osm_data import country_list_to_geofk
        
        test_cases = [
            (["CO"], ["colombia"]),
            (["BR"], ["brazil"]),
            (["CO", "PE"], ["colombia", "peru"]),
        ]
        
        for input_countries, expected in test_cases:
            result = country_list_to_geofk(input_countries)
            if result == expected:
                print(f"✓ Country mapping test passed: {input_countries} -> {result}")
            else:
                print(f"✗ Country mapping test failed: {input_countries} -> {result} (expected {expected})")
                return False
        
        return True
    except Exception as e:
        print(f"✗ Country mapping test failed: {e}")
        return False

def test_config_structure():
    """Test that config structure can be loaded"""
    try:
        import yaml
        config_path = Path(__file__).parent.parent / "configs" / "config.base.yaml"
        
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
        
        # Check for required keys
        required_keys = ["countries", "osm_data"]
        for key in required_keys:
            if key not in config:
                print(f"✗ Missing required config key: {key}")
                return False
        
        # Check OSM data config
        osm_config = config["osm_data"]
        expected_osm_keys = ["historical_date", "data_dir", "output_dir"]
        for key in expected_osm_keys:
            if key not in osm_config:
                print(f"✗ Missing OSM config key: {key}")
                return False
        
        print(f"✓ Config structure test passed")
        print(f"  Countries: {config['countries']}")
        print(f"  Historical date: {osm_config['historical_date']}")
        return True
        
    except Exception as e:
        print(f"✗ Config structure test failed: {e}")
        return False

def run_tests():
    """Run all tests"""
    print("Running fetch_osm_data tests...\n")
    
    tests = [
        ("Import test", test_fetch_osm_data_import),
        ("Country mapping test", test_country_mapping),
        ("Config structure test", test_config_structure),
    ]
    
    passed = 0
    total = len(tests)
    
    for name, test_func in tests:
        print(f"Running {name}...")
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"✗ {name} failed with exception: {e}")
        print()
    
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        return True
    else:
        print("❌ Some tests failed")
        return False

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)