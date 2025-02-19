import time

data_collections = {
    "Sentinel2": {
        "collection_name": "COPERNICUS/S2",
        "data_type": "vegetation",
        "RGB_bands": ["B4", "B3", "B2"],
        "NIR_band": "B8",
        "mask_cloud": True,
        "cloudy_pix_frac": 50,
        "cloudy_pix_flag": "CLOUDY_PIXEL_PERCENTAGE",
        "min_date": "2016-01-01",
        "max_date": "2022-01-01",  # Get to current year.
        #        "max_date": time.strftime("%Y-%m-%d"),
        "time_per_point": "1m",
    },
    "Landsat8": {
        "collection_name": "LANDSAT/LC08/C01/T1_SR",
        "data_type": "vegetation",
        "RGB_bands": ["B4", "B3", "B2"],
        "NIR_band": "B5",
        "cloudy_pix_flag": "CLOUD_COVER",
        "min_date": "2013-01-01",
        "max_date": time.strftime("%Y-%m-%d"),
        "time_per_point": "1m",
    },
    "Landsat7": {
        "collection_name": "LANDSAT/LE07/C01/T1_SR",
        "data_type": "vegetation",
        "RGB_bands": ["B3", "B2", "B1"],
        "NIR_band": "B4",
        "cloudy_pix_flag": "CLOUD_COVER",
        "min_date": "1999-01-01",
        "max_date": time.strftime("%Y-%m-%d"),
        "time_per_point": "1m",
    },
    "Landsat5": {
        "collection_name": "LANDSAT/LT05/C01/T1_SR",
        "data_type": "vegetation",
        "RGB_bands": ["B3", "B2", "B1"],
        "NIR_band": "B4",
        "cloudy_pix_flag": "None",
        "min_date": "1984-01-01",
        "max_date": "2013-01-01",
        "time_per_point": "1m",
    },
    "Landsat4": {
        "collection_name": "LANDSAT/LT04/C01/T1_SR",
        "data_type": "vegetation",
        "RGB_bands": ["B3", "B2", "B1"],
        "NIR_band": "B4",
        "cloudy_pix_flag": "None",
        "min_date": "1982-01-01",
        "max_date": "1994-01-01",
        "time_per_point": "1m",
    },
    "ERA5": {
        "collection_name": "ECMWF/ERA5/MONTHLY",
        "data_type": "weather",
        "precipitation_band": ["total_precipitation"],
        "temperature_band": ["mean_2m_air_temperature"],
        "min_date": "1986-01-01",
        "max_date": "2020-01-01",
        #        "max_date": time.strftime("%Y-%m-%d"),
        "time_per_point": "1m",
    },
    "ERA5_daily": {
        "collection_name": "ECMWF/ERA5/DAILY",
        "data_type": "weather",
        "precipitation_band": ["total_precipitation"],
        "temperature_band": ["mean_2m_air_temperature"],
        "min_date": "1986-01-01",
        "max_date": time.strftime("%Y-%m-%d"),
        "time_per_point": "1w",
    },
}
