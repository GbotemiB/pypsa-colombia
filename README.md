# PyPSA-Colombia
Energy Modeling Case Study for Colombia

## Getting Started

### Cloning the Repository

This repository uses Git submodules. To clone the repository along with its submodules, use the following command:

```bash
git clone --recursive https://github.com/pypsa-meets-earth/pypsa-colombia.git
```

If you have already cloned the repository without the `--recursive` flag, you can initialize and update the submodules with:

```bash
git submodule update --init --recursive
```

### Installation

1. Clone the repository as described above.
2. Navigate to the project directory:
   ```bash
   cd pypsa-colombia
   ```
3. Install the necessary dependencies using `conda` or `mamba`:

    mamba env create -f submodules/pypsa-earth-osm/envs/environment.yaml

4. You can check the (documentation)(https://pypsa-earth.readthedocs.io/en/latest/installation.html#install-dependencies) to install using lockfiles for your OS.

5.  Activate `pypsa-earth` environment:
    ```bash
    conda activate pypsa-earth
    ```
Note! At the moment, head of the PyPSA-Earth-osm submodule points to main branch of [PyPSA-meets-Earth/pypsa-earth-osm](https://github.com/pypsa-meets-earth/pypsa-earth-osm) repository.

### Running the model

This project utilizes [`snakemake`](https://snakemake.readthedocs.io/en/stable/) to automate the execution of scripts, ensuring efficient and reproducible workflows. 

To run the power model for the base scenario, use the following command from the root directory:

(Optional) For a dry-run, use the following command `snakemake -call solve_all_networks --configfile configs/config.base.yaml -n`


```bash
snakemake -call solve_all_networks --configfile configs/config.base.yaml  
```