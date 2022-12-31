import datetime
import os
import subprocess

import matplotlib.pyplot as plt
import numpy as np
from sentinelhub import (CRS, BBox, DataCollection, DownloadRequest, MimeType,
                         MosaickingOrder, SentinelHubDownloadClient,
                         SentinelHubRequest, SHConfig, bbox_to_dimensions)

from utils import *

config = SHConfig()

if not config.sh_client_id or not config.sh_client_secret:
    # If not set then update the SHConfiguration for Process API
    print("Setting.......")
    config.instance_id = ""
    config.sh_client_id = ""
    config.sh_client_secret = ""
    config.save()


betsiboka_coords_wgs84 = [46.16, -16.15, 46.51, -15.58]
resolution = 60
betsiboka_bbox = BBox(bbox=betsiboka_coords_wgs84, crs=CRS.WGS84)
betsiboka_size = bbox_to_dimensions(betsiboka_bbox, resolution=resolution)

print(f"Image shape at {resolution} m resolution: {betsiboka_size} pixels")

evalscript_true_color = """
    //VERSION=3

    function setup() {
        return {
            input: [{
                bands: ["B02", "B03", "B04"]
            }],
            output: {
                bands: 3
            }
        };
    }

    function evaluatePixel(sample) {
        return [sample.B04, sample.B03, sample.B02];
    }
"""

request_true_color = SentinelHubRequest(
    data_folder="./data/",
    evalscript=evalscript_true_color,
    input_data=[
        SentinelHubRequest.input_data(
            data_collection=DataCollection.SENTINEL2_L1C,
            time_interval=("2020-06-12", "2020-06-13"),
        )
    ],
    responses=[SentinelHubRequest.output_response("default", MimeType.TIFF)],
    bbox=betsiboka_bbox,
    size=betsiboka_size,
    config=config,
)

true_color_imgs = request_true_color.get_data(save_data=True)

"""
Use this for single image
convert_to_thumbnail(
    "data/d19514cf33acf6fe96e66c4f12ee1085/response.tiff",
    "data/d19514cf33acf6fe96e66c4f12ee1085/response.webp",
)

convert_to_cog(
    "data/d19514cf33acf6fe96e66c4f12ee1085/response.tiff",
    "data/d19514cf33acf6fe96e66c4f12ee1085/response_cog.tiff",
)
"""


convert_all_tiff_to_thumbnail_and_cog(data_dir="./data/")
