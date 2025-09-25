# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: PyPSA-Colombia Contributors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

"""
Simple script to fetch OSM data using earth-osm's save_osm_data function.
This script allows fetching OSM data for a specific date using the historical data feature.
"""

import argparse
import logging
import os
import yaml
from pathlib import Path
from datetime import datetime

# Import earth-osm functions
try:
    from earth_osm import eo
except ImportError as e:
    raise ImportError("earth-osm package is required. Please install it.") from e


def setup_logging():
    """Set up logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    return logging.getLogger(__name__)


def country_list_to_geofk(country_list):
    """
    Convert the requested country list into geofk norm.
    """
    # Simple mapping for common countries
    mapping = {
        'CO': 'colombia',
        'BR': 'brazil',
        'AR': 'argentina',
        'PE': 'peru',
        'VE': 'venezuela',
        'EC': 'ecuador',
        'CL': 'chile',
        'BO': 'bolivia',
        'UY': 'uruguay',
        'PY': 'paraguay'
    }
    
    # Convert country codes to geofk format
    geofk_list = []
    for country in country_list:
        if isinstance(country, str) and len(country) == 2:
            geofk_name = mapping.get(country.upper())
            if geofk_name:
                geofk_list.append(geofk_name)
            else:
                geofk_list.append(country.lower())
        else:
            geofk_list.append(country)
    
    return geofk_list


def fetch_osm_data(countries, target_date=None, data_dir="data/osm", output_dir="resources/osm/raw", logger=None):
    """
    Fetch OSM data using earth-osm's save_osm_data function.
    
    Parameters:
    -----------
    countries : list
        List of country codes (e.g., ["CO", "PE"])
    target_date : str, optional
        Target date for historical data in YYYY-MM-DD format
    data_dir : str
        Directory to store raw OSM data
    output_dir : str
        Directory to store processed OSM data
    logger : logging.Logger, optional
        Logger instance
    
    Returns:
    --------
    bool : True if successful, False otherwise
    """
    if logger is None:
        logger = setup_logging()
    
    try:
        # Create directories
        Path(data_dir).mkdir(parents=True, exist_ok=True)
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Convert countries to geofk format
        region_list = country_list_to_geofk(countries)
        
        logger.info(f"Fetching OSM data for regions: {region_list}")
        if target_date:
            logger.info(f"Target date: {target_date}")
        
        # Prepare save_osm_data parameters
        save_params = {
            'primary_name': "power",
            'region_list': region_list,
            'feature_list': ["substation", "line", "cable", "generator"],
            'update': False,
            'mp': True,
            'data_dir': data_dir,
            'out_dir': output_dir,
            'out_format': ["csv", "geojson"],
            'out_aggregate': True,
            'progress_bar': True,
        }
        
        # Add date parameter if provided
        if target_date:
            try:
                # Validate date format
                datetime.strptime(target_date, '%Y-%m-%d')
                save_params['date'] = target_date
                logger.info(f"Using historical data for date: {target_date}")
            except ValueError:
                logger.error(f"Invalid date format: {target_date}. Expected YYYY-MM-DD")
                return False
        
        # Call save_osm_data
        logger.info("Starting OSM data download...")
        eo.save_osm_data(**save_params)
        logger.info("OSM data download completed successfully")
        
        # Handle empty files (similar to the original download script)
        out_path = Path(output_dir) / "out"
        names = ["generator", "cable", "line", "substation"]
        out_formats = ["csv", "geojson"]
        
        if out_path.exists():
            for name in names:
                for fmt in out_formats:
                    new_file_name = Path(output_dir) / f"all_raw_{name}s.{fmt}"
                    old_files = list(out_path.glob(f"*{name}.{fmt}"))
                    
                    # If file is missing, create empty file, otherwise move it
                    if not old_files:
                        logger.info(f"Creating empty file: {new_file_name}")
                        new_file_name.touch()
                    else:
                        logger.info(f"Moving {old_files[0]} to {new_file_name}")
                        old_files[0].rename(new_file_name)
        
        return True
        
    except Exception as e:
        logger.error(f"Error fetching OSM data: {e}")
        return False


def main():
    """Main function for command line interface."""
    parser = argparse.ArgumentParser(
        description="Fetch OSM data using earth-osm's save_osm_data function"
    )
    parser.add_argument(
        "--countries", 
        nargs="+", 
        default=["CO"],
        help="List of country codes (default: ['CO'])"
    )
    parser.add_argument(
        "--date", 
        type=str, 
        default=None,
        help="Target date for historical data (YYYY-MM-DD format)"
    )
    parser.add_argument(
        "--data-dir", 
        type=str, 
        default="data/osm",
        help="Directory to store raw OSM data"
    )
    parser.add_argument(
        "--output-dir", 
        type=str, 
        default="resources/osm/raw",
        help="Directory to store processed OSM data"
    )
    parser.add_argument(
        "--config",
        type=str,
        default="configs/config.base.yaml",
        help="Path to configuration file"
    )
    
    # Check if running from Snakemake
    try:
        snakemake
        is_snakemake = True
    except NameError:
        is_snakemake = False
    
    if not is_snakemake:
        # Command line execution
        args = parser.parse_args()
        logger = setup_logging()
        
        # Try to load config file if it exists
        config_path = Path(args.config)
        countries = args.countries
        target_date = args.date
        data_dir = args.data_dir
        output_dir = args.output_dir
        
        if config_path.exists():
            try:
                with open(config_path, "r") as f:
                    config = yaml.safe_load(f)
                
                # Override with config values if available
                countries = config.get("countries", countries)
                
                # Check for OSM data configuration
                osm_config = config.get("osm_data", {})
                if not target_date and osm_config.get("historical_date"):
                    target_date = osm_config.get("historical_date")
                if osm_config.get("data_dir"):
                    data_dir = osm_config.get("data_dir", data_dir)
                if osm_config.get("output_dir"):
                    output_dir = osm_config.get("output_dir", output_dir)
                    
            except Exception as e:
                logger.warning(f"Could not load config file {config_path}: {e}")
        
        # Fetch the data
        success = fetch_osm_data(countries, target_date, data_dir, output_dir, logger)
        
        if success:
            logger.info("OSM data fetch completed successfully")
        else:
            logger.error("OSM data fetch failed")
            exit(1)
            
    else:
        # Running from Snakemake
        logger = setup_logging()
        
        countries = snakemake.params.countries
        target_date = snakemake.params.get("target_date", None)
        data_dir = snakemake.params.get("data_dir", "data/osm")
        output_dir = snakemake.params.get("output_dir", "resources/osm/raw")
        
        success = fetch_osm_data(countries, target_date, data_dir, output_dir, logger)
        
        if not success:
            raise RuntimeError("OSM data fetch failed")


if __name__ == "__main__":
    main()