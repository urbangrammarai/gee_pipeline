# config file for running pyveg_run_pipeline
##
# This file was generated from the command
# pyveg_generate_config
# on 22-07-29 15:31:45

from pyveg.configs.collections import data_collections

# this name doesn't do anything - it's just an id given to the Pipeline instance
name = "pyveg"

# Define location to save all outputs.   Note that every time the pipeline job
# is rerun, a datestamp will be appended to the output_location.
output_location = "./Sentinel2-52.50N-1.90W-birmingham-reproject-test"
output_location_type = "local"

# parse selection. Note (long, lat) GEE convention.
coordinates = (-1.90, 52.50)

# optional coords_id setting


# pattern_type description
pattern_type = "unknown"

date_range = ["2019-01-01", "2019-09-30"]

# From the dictionary entries in data_collections.py, which shall we use
# (these will become "Sequences")
collections_to_use = ["Sentinel2"]

# Dictionary defining what Modules should run in each Sequence.

modules_to_use = {
    "Sentinel2": [
        "VegetationDownloader",
        "Reprojector",
        "VegetationImageProcessor",
    ]
}

# The following demonstrates how parameters can be set for individual Modules:
special_config = {
    "Sentinel2": {
        "time_per_point": "3m"
    },
    "VegetationDownloader": {"region_size": 0.08},
    "VegetationImageProcessor": {"run_mode": "local"},
}
