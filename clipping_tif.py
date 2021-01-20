import rasterio
from rasterio.mask import mask
import numpy as np


def zone_defining(tif_file, shape):

    out_image, out_transform = rasterio.mask.mask(tif_file, shapes=shape, all_touched=True, crop=True)
    out_datas = tif_file.meta
    out_image = np.moveaxis(out_image.squeeze(), 1, 0)

    return out_image, out_datas




