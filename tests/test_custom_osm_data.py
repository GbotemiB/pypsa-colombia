# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: PyPSA-Colombia Contributors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

"""
Unit tests for custom_osm_data.py using enhanced earth-osm package.
"""

from custom_osm_data import (
    setup_logging,
    country_code_to_region_name,
    download_osm_data_for_country,
    main
)
import unittest
import tempfile
import os
from unittest.mock import patch, MagicMock
import sys

# Add the scripts directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))


class TestCustomOsmData(unittest.TestCase):
    """Test cases for the custom OSM data download functionality."""

    def test_setup_logging(self):
        """Test that logging is set up correctly."""
        logger = setup_logging()
        self.assertIsNotNone(logger)
        self.assertEqual(logger.name, 'custom_osm_data')

    def test_country_code_to_region_name(self):
        """Test country code to region name conversion."""
        self.assertEqual(country_code_to_region_name('CO'), 'colombia')
        self.assertEqual(country_code_to_region_name('BR'), 'brazil')
        self.assertEqual(country_code_to_region_name('AR'), 'argentina')
        self.assertEqual(country_code_to_region_name(
            'XX'), 'xx')  # Unknown country

    @patch('custom_osm_data.get_region_tuple')
    def test_download_data_failure(self, mock_get_region_tuple):
        """Test handling of download failures."""
        mock_get_region_tuple.side_effect = Exception("Region not found")

        with tempfile.TemporaryDirectory() as temp_dir:
            config = {'download_historical': False}
            logger = setup_logging()

            results = download_osm_data_for_country(
                'CO', config, temp_dir, logger)

            self.assertFalse(results['pbf'])
            self.assertFalse(results['md5'])
            self.assertFalse(results['power.json'])

    @patch('custom_osm_data.download_osm_data_for_country')
    def test_main_function(self, mock_download_function):
        """Test the main function with multiple countries."""
        mock_download_function.return_value = {
            'pbf': True,
            'md5': True,
            'power.json': False
        }

        countries = ['CO', 'BR']
        config = {'download_historical': False}

        with tempfile.TemporaryDirectory() as temp_dir:
            results = main(countries, config, temp_dir)

            self.assertEqual(len(results), 2)
            self.assertIn('CO', results)
            self.assertIn('BR', results)
            self.assertEqual(mock_download_function.call_count, 2)


if __name__ == '__main__':
    unittest.main()
