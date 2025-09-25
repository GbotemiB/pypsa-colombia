#!/usr/bin/env python3
"""
Demonstration script for fetch_osm_data functionality
"""

import sys
from pathlib import Path
import tempfile
import shutil

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

def demo_basic_usage():
    """Demonstrate basic usage of fetch_osm_data"""
    print("=== fetch_osm_data Basic Usage Demo ===\n")
    
    try:
        from fetch_osm_data import fetch_osm_data, setup_logging, country_list_to_geofk
        
        # Setup logging
        logger = setup_logging()
        
        print("1. Country code mapping:")
        test_countries = ["CO", "PE", "BR"]
        mapped = country_list_to_geofk(test_countries)
        print(f"   {test_countries} -> {mapped}")
        
        print("\n2. Configuration example:")
        print("   Add to your configs/config.base.yaml:")
        print("   osm_data:")
        print("     historical_date: '2020-01-01'")
        print("     data_dir: 'data/osm'")
        print("     output_dir: 'resources/osm/raw'")
        
        print("\n3. Command line usage examples:")
        print("   # Basic usage:")
        print("   python scripts/fetch_osm_data.py")
        print()
        print("   # With specific date and countries:")
        print("   python scripts/fetch_osm_data.py --countries CO PE --date 2020-01-01")
        print()
        print("   # Using config file:")
        print("   python scripts/fetch_osm_data.py --config configs/config.base.yaml")
        
        print("\n4. Snakemake integration:")
        print("   # Run fetch_osm_data rule:")
        print("   snakemake --cores 1 fetch_osm_data")
        print()
        print("   # Run complete workflow:")
        print("   snakemake --cores 4 clean_osm_data")
        
        print("\n5. Expected output files:")
        expected_outputs = [
            "all_raw_cables.geojson",
            "all_raw_generators.geojson", 
            "all_raw_generators.csv",
            "all_raw_lines.geojson",
            "all_raw_substations.geojson"
        ]
        for output in expected_outputs:
            print(f"   - {output}")
        
        print("\n✓ Demo completed successfully!")
        print("\nNote: To actually download data, you need:")
        print("- earth-osm package installed")
        print("- Internet connection")
        print("- Sufficient disk space")
        
        return True
        
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False
    except Exception as e:
        print(f"✗ Demo failed: {e}")
        return False

def demo_configuration():
    """Demonstrate configuration loading"""
    print("\n=== Configuration Demo ===\n")
    
    try:
        import yaml
        
        config_path = Path(__file__).parent.parent / "configs" / "config.base.yaml"
        print(f"Loading config from: {config_path}")
        
        if not config_path.exists():
            print("✗ Config file not found")
            return False
        
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
        
        print("\nConfiguration loaded:")
        print(f"  Countries: {config.get('countries', 'Not set')}")
        
        osm_config = config.get('osm_data', {})
        print(f"  OSM Data Config:")
        print(f"    Historical Date: {osm_config.get('historical_date', 'Not set')}")
        print(f"    Data Dir: {osm_config.get('data_dir', 'Not set')}")
        print(f"    Output Dir: {osm_config.get('output_dir', 'Not set')}")
        
        print("\n✓ Configuration demo completed successfully!")
        return True
        
    except Exception as e:
        print(f"✗ Configuration demo failed: {e}")
        return False

def demo_file_structure():
    """Show the expected file structure"""
    print("\n=== File Structure Demo ===\n")
    
    project_root = Path(__file__).parent.parent
    print(f"Project root: {project_root}")
    
    important_files = [
        "scripts/fetch_osm_data.py",
        "configs/config.base.yaml", 
        "Snakefile",
        "doc/fetch_osm_data.md",
        "tests/test_fetch_osm_data.py"
    ]
    
    print("\nImportant files:")
    all_exist = True
    for file_path in important_files:
        full_path = project_root / file_path
        exists = full_path.exists()
        status = "✓" if exists else "✗"
        print(f"  {status} {file_path}")
        if not exists:
            all_exist = False
    
    if all_exist:
        print("\n✓ All required files present!")
    else:
        print("\n⚠ Some files are missing")
    
    return all_exist

def main():
    """Run all demos"""
    print("PyPSA-Colombia fetch_osm_data Demonstration\n")
    print("=" * 50)
    
    demos = [
        ("Basic Usage", demo_basic_usage),
        ("Configuration", demo_configuration), 
        ("File Structure", demo_file_structure),
    ]
    
    results = []
    for name, demo_func in demos:
        print(f"\n{name} Demo:")
        print("-" * 20)
        try:
            result = demo_func()
            results.append(result)
        except Exception as e:
            print(f"✗ {name} demo failed with exception: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Demos completed: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 All demos completed successfully!")
        print("\nYour fetch_osm_data setup is ready to use!")
        print("\nNext steps:")
        print("1. Install required dependencies (earth-osm, pyyaml)")
        print("2. Run: python scripts/fetch_osm_data.py")
        print("3. Or use Snakemake: snakemake fetch_osm_data")
    else:
        print("\n❌ Some issues detected")
        print("Please check the error messages above")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)