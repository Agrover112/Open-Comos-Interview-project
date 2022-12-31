# Description: Utility functions for the project
import os
from typing import Any, Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np
import PIL
from PIL import Image


def plot_image(
    image: np.ndarray,
    factor: float = 1.0,
    clip_range: Optional[Tuple[float, float]] = None,
    **kwargs: Any
) -> None:
    """
    Plot an image using matplotlib
    """
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(15, 15))
    if clip_range is not None:
        ax.imshow(np.clip(image * factor, *clip_range), **kwargs)
    else:
        ax.imshow(image * factor, **kwargs)
    ax.set_xticks([])
    ax.set_yticks([])


def convert_to_thumbnail(img_path, new_path, mask=True) -> None:
    """
    Convert image to thumbnail
    """
    img = Image.open(img_path)
    img = img.convert("RGBA")
    img.thumbnail(size=((500, 500)))

    if mask:
        # Transparency
        newImage = []
        for item in img.getdata():
            if item[:3] == (0, 0, 0):  # If Pixel values are 0 (Black)
                newImage.append((0, 0, 0, 0))
            else:
                newImage.append(item)  # Pixels values  present

        img.putdata(newImage)

    img.save(new_path, "webp", quality=95)


def convert_to_cog(img_path, new_path) -> None:
    """Convert Tiff to COG"""
    os.system(
        "gdal_translate -of GTiff -co TILED=YES -co COPY_SRC_OVERVIEWS=YES -co COMPRESS=LZW {} {}".format(
            img_path, new_path
        )
    )


def convert_all_tiff_to_thumbnail_and_cog(data_dir="./data/"):
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if file.endswith(".tiff"):
                convert_to_thumbnail(
                    os.path.join(root, file),
                    os.path.join(root, file.replace(".tiff", ".webp")),
                )
                convert_to_cog(
                    os.path.join(root, file),
                    os.path.join(root, file.replace(".tiff", "_cog.tiff")),
                )
