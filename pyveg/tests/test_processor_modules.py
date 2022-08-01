"""
Tests for the modules that process the images downloaded from GEE
"""

import json
import os
import shutil
from pathlib import Path

import pytest
from icecream import ic

from pyveg.src.processor_modules import (
    NDVICalculator,
    NetworkCentralityCalculator,
    Reprojector,
    VegetationImageProcessor,
    WeatherImageToJSON,
)


@pytest.mark.skipif(
    os.environ.get("CI") == "true",
    reason="Skipping this test in a CI - waiting on a fix for #20. https://github.com/urbangrammarai/gee_pipeline/issues/20",
)
def test_Sentinel2_image_processor():
    """
    Should combine tif files into RGB, NDVI, and BWNDVI
    big images, and split RGB and BWNVI into sub-images.
    """
    dir_path = os.path.join(
        os.path.dirname(__file__), "..", "testdata", "Sentinel2", "test_tif"
    )
    tmp_png_path = os.path.join(
        os.path.dirname(__file__), "..", "testdata", "Sentinel2", "tmp_png"
    )

    vip = VegetationImageProcessor()
    vip.input_location = dir_path
    vip.output_location = tmp_png_path
    vip.ndvi = True
    vip.coords = [11.58, 27.95]
    vip.configure()
    vip.run()
    assert os.path.exists(os.path.join(tmp_png_path, "2018-03-01", "PROCESSED"))
    assert len(os.listdir(os.path.join(tmp_png_path, "2018-03-01", "PROCESSED"))) == 3
    assert os.path.exists(os.path.join(tmp_png_path, "2018-03-01", "SPLIT"))
    assert len(os.listdir(os.path.join(tmp_png_path, "2018-03-01", "SPLIT"))) == 1452
    shutil.rmtree(tmp_png_path, ignore_errors=True)


def test_ERA5_image_to_json():
    """
    Get values out of tif files and put into JSON file.
    """
    dir_path = os.path.join(
        os.path.dirname(__file__), "..", "testdata", "ERA5", "test_tif"
    )
    tmp_json_path = os.path.join(
        os.path.dirname(__file__), "..", "testdata", "ERA5", "tmp_json"
    )

    wip = WeatherImageToJSON()
    wip.input_location = dir_path
    wip.output_location = tmp_json_path
    wip.coords = [11.58, 27.95]
    wip.configure()
    wip.run()
    assert os.path.exists(
        os.path.join(
            tmp_json_path, "2016-01-16", "JSON", "WEATHER", "weather_data.json"
        )
    )
    results = json.load(
        open(
            os.path.join(
                tmp_json_path, "2016-01-16", "JSON", "WEATHER", "weather_data.json"
            )
        )
    )
    #    assert "2016-01-16" in results.keys()
    assert "mean_2m_air_temperature" in results.keys()
    assert "total_precipitation" in results.keys()
    assert isinstance(results["mean_2m_air_temperature"], float)
    assert isinstance(results["total_precipitation"], float)
    shutil.rmtree(tmp_json_path)


def test_NetworkCentralityCalculator():
    """
    Test that we can go from a directory containing some 50x50 BWNVI images
    to a json file containing network centrality values.
    """
    dir_path = os.path.join(
        os.path.dirname(__file__), "..", "testdata", "Sentinel2", "test_png"
    )
    tmp_json_path = os.path.join(
        os.path.dirname(__file__), "..", "testdata", "Sentinel2", "tmp_json"
    )
    ncc = NetworkCentralityCalculator()
    ncc.input_location = dir_path
    ncc.output_location = tmp_json_path
    ncc.configure()
    ncc.run()
    assert os.path.exists(
        os.path.join(
            tmp_json_path, "2018-03-01", "JSON", "NC", "network_centralities.json"
        )
    )
    nc_json = json.load(
        open(
            os.path.join(
                tmp_json_path, "2018-03-01", "JSON", "NC", "network_centralities.json"
            )
        )
    )
    assert isinstance(nc_json, list)
    assert isinstance(nc_json[0], dict)
    # test float values
    for key in ["latitude", "longitude", "offset50"]:
        assert key in nc_json[0].keys()
        assert isinstance(nc_json[0][key], float)
        assert nc_json[0][key] != 0.0
    assert "date" in nc_json[0].keys()
    assert isinstance(nc_json[0]["date"], str)
    shutil.rmtree(tmp_json_path)


def test_NDVICalculator():
    """
    Test that we can go from a directory containing some 50x50 BWNVI images
    to a json file containing network centrality values.
    """
    dir_path = os.path.join(
        os.path.dirname(__file__), "..", "testdata", "Sentinel2", "test_png"
    )
    tmp_json_path = os.path.join(
        os.path.dirname(__file__), "..", "testdata", "Sentinel2", "tmp_json"
    )
    ndvic = NDVICalculator()
    ndvic.input_location = dir_path
    ndvic.output_location = tmp_json_path
    ndvic.configure()
    ndvic.run()
    assert os.path.exists(
        os.path.join(tmp_json_path, "2018-03-01", "JSON", "NDVI", "ndvi_values.json")
    )
    nc_json = json.load(
        open(
            os.path.join(
                tmp_json_path, "2018-03-01", "JSON", "NDVI", "ndvi_values.json"
            )
        )
    )
    assert isinstance(nc_json, list)
    assert isinstance(nc_json[0], dict)
    # test float values
    for key in ["latitude", "longitude", "ndvi", "ndvi_veg"]:
        assert key in nc_json[0].keys()
        assert isinstance(nc_json[0][key], float)
        assert nc_json[0][key] != 0.0
    assert "date" in nc_json[0].keys()
    assert isinstance(nc_json[0]["date"], str)
    shutil.rmtree(tmp_json_path)


def test_Reprojector(tmp_path):
    input_path = (
        Path(__file__).parent.parent / "testdata" / "Sentinel2" / "test_ne_england"
    )
    ic(input_path)

    tmp_output_path = tmp_path / "2018-03-01" / "projected"

    repoj = Reprojector()
    repoj.input_location = str(input_path)
    repoj.output_location = str(tmp_path)
    repoj.ndvi = True
    repoj.coords = [11.58, 27.95]
    repoj.configure()
    repoj.run()

    # check module repoj.run_status
    ic(repoj.run_status)

    expected_run_status = {"failed": 0, "incomplete": 0, "succeeded": 1}
    assert repoj.run_status == expected_run_status

    # Check that the output dir was created correctly
    assert tmp_output_path.exists()
    assert tmp_output_path.is_dir()

    # Check that the output dir contains the expected number of files
    assert len([f for f in tmp_output_path.iterdir()]) == 2

    """
    (gee_pipeline) T0QGJHN936:RAW a.smith$ rio info ne_mosaic_bng.tif
    {"blockxsize": 256, "blockysize": 256, "bounds": [409955.8954843804, 548977.8478618148, 443001.9881505056, 574618.0929891961], "colorinterp": ["gray", "undefined", "undefined"], "count": 3, "crs": "EPSG:27700", "descriptions": [null, null, null], "driver": "GTiff", "dtype": "uint16", "height": 2562, "indexes": [1, 2, 3], "interleave": "pixel", "lnglat": [-1.5881173224112388, 54.95013449122592], "mask_flags": [["nodata"], ["nodata"], ["nodata"]], "nodata": 0.0, "res": [10.007902079383756, 10.0079020793838], "shape": [2562, 3302], "tiled": true, "transform": [10.007902079383756, 0.0, 409955.8954843804, 0.0, -10.0079020793838, 574618.0929891961, 0.0, 0.0, 1.0], "units": [null, null, null], "width": 3302}
    (gee_pipeline) T0QGJHN936:RAW a.smith$ rio info ne_mosaic_ll.tif
    {"blockxsize": 256, "blockysize": 256, "bounds": [-1.846526138233316, 54.83385086180488, -1.3282765593168353, 55.065937129126056], "colorinterp": ["gray", "undefined", "undefined"], "count": 3, "crs": "EPSG:4326", "descriptions": [null, null, null], "driver": "GTiff", "dtype": "uint16", "height": 1721, "indexes": [1, 2, 3], "interleave": "pixel", "lnglat": [-1.5874013487750758, 54.94989399546547], "mask_flags": [["nodata"], ["nodata"], ["nodata"]], "nodata": 0.0, "res": [0.00013485547200532938, 0.00013485547200532938], "shape": [1721, 3843], "tiled": true, "transform": [0.00013485547200532938, 0.0, -1.846526138233316, 0.0, -0.00013485547200532938, 55.065937129126056, 0.0, 0.0, 1.0], "units": [null, null, null], "width": 3843}

    """
