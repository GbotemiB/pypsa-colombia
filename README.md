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
3a. Install the necessary dependencies using `conda` or `mamba`:

    mamba env create -f submodules/pypsa-earth-osm/envs/environment.yaml

3b. You can check the (documentation)(https://pypsa-earth.readthedocs.io/en/latest/installation.html#install-dependencies) to install using lockfiles for your OS

4.  Activate `pypsa-earth` environment:
    ```bash
    conda activate pypsa-earth
    ```
Note! At the moment, head of the PyPSA-Earth-osm submodule points to main branch of [PyPSA-meets-Earth/pypsa-earth-osm](https://github.com/pypsa-meets-earth/pypsa-earth-osm) repository.