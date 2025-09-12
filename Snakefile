# SPDX-FileCopyrightText:  Open Energy Transition gGmbH
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from snakemake.utils import min_version
min_version("6.0")

import sys
sys.path.append("submodules/pypsa-earth-osm")
sys.path.append("submodules/pypsa-earth-osm/scripts")

from snakemake.remote.HTTP import RemoteProvider as HTTPRemoteProvider

HTTP = HTTPRemoteProvider()

RESULTS_DIR = "plots/results/"
PYPSA_EARTH_DIR = "submodules/pypsa-earth-osm/"


configfile: "submodules/pypsa-earth-osm/config.default.yaml"
configfile: "submodules/pypsa-earth-osm/configs/bundle_config.yaml"
configfile: "configs/config.base.yaml"

wildcard_constraints:
    simpl="[a-zA-Z0-9]*|all",
    clusters="[0-9]+(m|flex)?|all|min",
    ll="(v|c)([0-9\.]+|opt|all)|all",
    opts="[-+a-zA-Z0-9\.]*",
    unc="[-+a-zA-Z0-9\.]*",
    planning_horizon="[0-9]{4}",
    countries="[A-Z]{2}",


run = config["run"]
RDIR = run["name"] + "/" if run.get("name") else ""
CDIR = RDIR if not run.get("shared_cutouts") else ""
SECDIR = run["sector_name"] + "/" if run.get("sector_name") else ""
SDIR = config["summary_dir"].strip("/") + f"/{SECDIR}"
RESDIR = config["results_dir"].strip("/") + f"/{SECDIR}"

module pypsa_earth:
    snakefile:
        "submodules/pypsa-earth-osm/Snakefile"
    config:
        config
    prefix:
        "submodules/pypsa-earth-osm"


use rule * from pypsa_earth


localrules:
    all,