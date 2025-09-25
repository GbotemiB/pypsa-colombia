# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: PyPSA-Colombia Contributors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

"""
Script to download historical OSM data using enhanced earth-osm package.
"""

import argparse
import logging
import os
import yaml
from datetime import datetime
from pathlib import Path

# Import enhanced earth-osm functions
try:
    import earth_osm as eo
    from earth_osm.gfk_data import get_region_tuple
    from earth_osm.gfk_download import download_pbf, download_file
except ImportError as e:
    raise ImportError("Enhanced earth-osm package is required.") from e


def setup_logging():
    """Set up logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    return logging.getLogger(__name__)


def country_code_to_region_name(country_code):
    """Convert country code to earth-osm region name."""
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
    return mapping.get(country_code.upper(), country_code.lower())


def download_osm_data_for_country(country_code, config, output_dir, logger):
    """Download OSM data files for a specific country using earth-osm."""
    try:
        # Convert country code to region name
        region_name = country_code_to_region_name(country_code)

        # Get region information
        region = get_region_tuple(region_name)

        is_historical = config.get('download_historical', False)
        historical_date = config.get('historical_date', None)
        download_power_json = config.get('download_power_json', True)

        results = {'pbf': False, 'md5': False, 'power.json': False}

        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Download PBF file
        try:
            if is_historical and historical_date:
                # For historical data
                logger.info(
                    f"Downloading historical OSM data for {region_name} ({historical_date})")
                date_formatted = datetime.strptime(
                    historical_date, '%Y-%m-%d').strftime('%y%m%d')

                # Construct historical URL
                base_url = region.urls['pbf'].replace(
                    '-latest.osm.pbf', f'-{date_formatted}.osm.pbf')

                # Download historical PBF
                pbf_file = download_file(
                    base_url, str(output_path), exists_ok=True)

                if pbf_file and os.path.exists(pbf_file):
                    results['pbf'] = True
                    logger.info(
                        f"Successfully downloaded historical PBF: {pbf_file}")

                    # Try to download MD5
                    md5_url = base_url + '.md5'
                    md5_file = download_file(
                        md5_url, str(output_path), exists_ok=True)
                    if md5_file and os.path.exists(md5_file):
                        results['md5'] = True
                        logger.info(
                            f"Successfully downloaded historical MD5: {md5_file}")

            else:
                # Download latest data
                logger.info(f"Downloading latest OSM data for {region_name}")
                pbf_file = download_pbf(
                    region.urls['pbf'],
                    update=True,
                    data_dir=str(output_path),
                    progress_bar=True
                )

                if pbf_file and os.path.exists(pbf_file):
                    results['pbf'] = True
                    results['md5'] = True  # download_pbf handles MD5
                    logger.info(
                        f"Successfully downloaded latest PBF: {pbf_file}")

            # Download power.json if requested
            if download_power_json:
                try:
                    if is_historical and historical_date:
                        date_formatted = datetime.strptime(
                            historical_date, '%Y-%m-%d').strftime('%y%m%d')
                        power_url = region.urls['pbf'].replace(
                            '-latest.osm.pbf', f'-{date_formatted}-power.json')
                    else:
                        power_url = region.urls['pbf'].replace(
                            '-latest.osm.pbf', '-power.json')

                    power_file = download_file(
                        power_url, str(output_path), exists_ok=True)
                    if power_file and os.path.exists(power_file):
                        results['power.json'] = True
                        logger.info(
                            f"Successfully downloaded power.json: {power_file}")

                except Exception as e:
                    logger.info(f"Power.json download failed: {e}")

        except Exception as e:
            logger.error(f"Error downloading OSM data: {e}")

        return results

    except Exception as e:
        logger.error(f"Failed to get region information: {e}")
        return {'pbf': False, 'md5': False, 'power.json': False}


def main(countries, osm_config, output_dir):
    """Main function to download OSM data for multiple countries."""
    logger = setup_logging()

    os.makedirs(output_dir, exist_ok=True)

    all_results = {}

    for country_code in countries:
        logger.info(f"Processing country: {country_code}")

        results = download_osm_data_for_country(
            country_code, osm_config, output_dir, logger
        )

        all_results[country_code] = results

        # Log results
        for file_type, success in results.items():
            status = "SUCCESS" if success else "FAILED"
            logger.info(f"  {file_type}: {status}")

    return all_results


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--countries", nargs="+", default=["CO"])
    parser.add_argument("--output-dir", default="data/osm")
    parser.add_argument("--historical", action="store_true")
    parser.add_argument("--date", default="2020-01-01")

    # Check if running from Snakemake
    try:
        snakemake
        is_snakemake = True
    except NameError:
        is_snakemake = False

    if not is_snakemake:
        args = parser.parse_args()

        # Try to load from config file first
        config_path = Path("configs/config.base.yaml")
        if config_path.exists():
            with open(config_path, "r") as f:
                config = yaml.safe_load(f)

            countries = config.get("countries", args.countries)
            osm_config = config.get("osm_data", {})
            output_dir = osm_config.get("data_dir", args.output_dir)

            # Override with command line args if provided
            if args.historical:
                osm_config['download_historical'] = True
                osm_config['historical_date'] = args.date
        else:
            # Use command line args
            countries = args.countries
            osm_config = {
                'download_historical': args.historical,
                'historical_date': args.date,
                'download_power_json': True,
                'data_dir': args.output_dir
            }
            output_dir = args.output_dir

        results = main(countries, osm_config, output_dir)
        print(f"Download results: {results}")
    else:
        # Running from Snakemake
        countries = snakemake.params.countries
        osm_config = snakemake.params.osm_data
        output_dir = snakemake.params.output_dir

        results = main(countries, osm_config, output_dir)
