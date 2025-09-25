# fetch_osm_data - OSM Data Fetching Tool

This document describes the `fetch_osm_data` script that allows you to fetch OpenStreetMap (OSM) data using the earth-osm package with support for historical data retrieval.

## Overview

The `fetch_osm_data.py` script is a simple and flexible tool for downloading OSM power infrastructure data. It uses the `save_osm_data` function from the earth-osm package and can be integrated into the PyPSA-Colombia workflow.

## Features

- **Historical Data Support**: Fetch OSM data for specific dates
- **Configuration-based**: Uses YAML configuration files
- **Snakemake Integration**: Can be run as part of a Snakemake workflow
- **Command Line Interface**: Also supports standalone command-line usage
- **Multiple Country Support**: Download data for multiple countries at once

## Configuration

Add the following section to your `configs/config.base.yaml`:

```yaml
# OSM data configuration
osm_data:
  historical_date: "2020-01-01"  # Date for historical OSM data (YYYY-MM-DD format)
  data_dir: "data/osm"          # Directory to store raw OSM data
  output_dir: "resources/osm/raw" # Directory to store processed OSM data
```

## Usage

### 1. Command Line Usage

Basic usage:
```bash
python scripts/fetch_osm_data.py
```

With custom parameters:
```bash
python scripts/fetch_osm_data.py --countries CO PE --date 2020-01-01 --data-dir data/osm --output-dir resources/osm/raw
```

With config file:
```bash
python scripts/fetch_osm_data.py --config configs/config.base.yaml
```

### 2. Snakemake Integration

The script is integrated as a Snakemake rule called `fetch_osm_data`. You can run it using:

```bash
snakemake --cores 1 fetch_osm_data
```

Or as part of a larger workflow:
```bash
snakemake --cores 4 clean_osm_data
```

## Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--countries` | List of country codes | `["CO"]` |
| `--date` | Target date for historical data (YYYY-MM-DD) | `None` (latest) |
| `--data-dir` | Directory for raw OSM data | `"data/osm"` |
| `--output-dir` | Directory for processed OSM data | `"resources/osm/raw"` |
| `--config` | Path to configuration file | `"configs/config.base.yaml"` |

## Output Files

The script generates the following files in the output directory:

- `all_raw_cables.geojson` - Cable infrastructure data
- `all_raw_generators.geojson` - Power generation facilities
- `all_raw_generators.csv` - Power generation facilities (CSV format)
- `all_raw_lines.geojson` - Transmission lines
- `all_raw_substations.geojson` - Substations and switching stations

## Examples

### Example 1: Fetch latest OSM data for Colombia
```bash
python scripts/fetch_osm_data.py --countries CO
```

### Example 2: Fetch historical data for multiple countries
```bash
python scripts/fetch_osm_data.py --countries CO PE BR --date 2020-01-01
```

### Example 3: Use custom directories
```bash
python scripts/fetch_osm_data.py --data-dir my_data/osm --output-dir my_output/osm
```

### Example 4: Run with Snakemake for the full workflow
```bash
# This will use the configuration from configs/config.base.yaml
snakemake --cores 1 fetch_osm_data

# Or run the complete cleaning workflow which depends on fetch_osm_data
snakemake --cores 2 clean_osm_data
```

## Integration with PyPSA-Colombia Workflow

The `fetch_osm_data` rule is integrated into the main Snakefile and will:

1. Read configuration from `configs/config.base.yaml`
2. Use the specified countries, date, and output directories
3. Generate the required raw OSM files
4. Log the process to `logs/fetch_osm_data.log`
5. Create benchmarking data in `benchmarks/fetch_osm_data`

The output files are compatible with the existing PyPSA-Earth workflow and can be used as input to the `clean_osm_data` rule.

## Dependencies

- `earth-osm` package
- `pyyaml` for configuration parsing
- `pathlib` and other standard Python libraries

## Error Handling

The script includes comprehensive error handling:

- Validates date format if provided
- Creates output directories if they don't exist
- Handles empty files (creates empty placeholders for Snakemake compatibility)
- Logs all operations and errors

## Testing

Run the test suite to validate the installation:

```bash
python3 tests/test_fetch_osm_data.py
```

This will test:
- Module imports
- Country code mapping
- Configuration file structure

## Comparison with custom_osm_data.py

| Feature | fetch_osm_data.py | custom_osm_data.py |
|---------|-------------------|-------------------|
| **Primary Purpose** | Simple OSM data fetching using earth-osm | Enhanced OSM data downloading with custom features |
| **Main Function** | Uses `eo.save_osm_data()` directly | Uses enhanced earth-osm functions like `download_pbf()` |
| **Historical Data** | Uses earth-osm's built-in `date` parameter | Custom historical data handling with URL construction |
| **File Handling** | Uses earth-osm's built-in aggregation | Custom file renaming and moving logic |
| **Complexity** | Simple and focused | More feature-rich with custom logic |
| **Integration** | Direct Snakemake integration | Supports both Snakemake and standalone |

Choose `fetch_osm_data.py` for simple, reliable OSM data fetching using the standard earth-osm interface. Choose `custom_osm_data.py` for more advanced features and custom data handling needs.