import logging
import numpy as np
import pandas as pd
from osgeo import gdal


class Logger(object):

    def __init__(self, level=logging.INFO):
        logfmt = "[%(asctime)s - %(levelname)s] - %(message)s"
        dtfmt = "%Y-%m-%d %I:%M:%S"
        logging.basicConfig(level=level, format=logfmt, datefmt=dtfmt)

    def get(self):
        return logging.getLogger()


class Raster2xyz(object):

    def __init__(self, verbose=True):
        if not verbose:
            lg = Logger(level=logging.ERROR)
        else:
            lg = Logger()

        self.__logger = lg.get()

    def __geotrCoords(self, gtr, x, y):
        """
        """
        try:
            self.__logger.info("Getting geotransformed coordinates...")

            gtr_x = x
            gtr_y = y
            return (gtr_x, gtr_y)

        except Exception as err:
            self.__logger.error("Error getting geotransformed coordinates: {0}".format(err))

    def __getRasterData(self, input_raster, n_band):
        """
        """
        try:
            self.__logger.info("Getting geotransform and data...")

            src_raster = gdal.Open(input_raster)
            raster_bnd = src_raster.GetRasterBand(n_band)

            raster_values = raster_bnd.ReadAsArray()
            gtr = src_raster.GetGeoTransform()

            src_raster = None

            return (gtr, raster_values)

        except Exception as err:
            self.__logger.error("Error getting geotransform and data: {0}".format(err))

    def __getXyzData(self, raster_values, no_data):
        """
        """
        try:
            self.__logger.info("Getting XYZ data...")

            y, x = np.where(raster_values != no_data)
            data_vals = np.extract(raster_values != no_data, raster_values)

            return (x, y, data_vals)

        except Exception as err:
            self.__logger.error("Error getting XYZ data: {0}".format(err))

    def __buildXyzData(self, gtr_x, gtr_y, data_vals):
        """
        """
        try:
            self.__logger.info("Building XYZ data...")

            data_dict = {
                "x": gtr_x,
                "y": gtr_y,
                "z": data_vals
            }

            return pd.DataFrame(data_dict)

        except Exception as err:
            self.__logger.error("Error building XYZ data: {0}".format(err))

    def __convert_meta(self, meta):
        return (meta[2], meta[0], meta[1], meta[5], meta[3], meta[4])

    def translate(self, crop_result, no_data=-9999):

        # Clean the received data
        raster, meta = crop_result
        meta = self.__convert_meta(meta['transform'])

        # Prepare the transformation
        x, y, data_vals = self.__getXyzData(raster, no_data)
        gtr_x, gtr_y = self.__geotrCoords(meta, x, y)

        return self.__buildXyzData(gtr_x, gtr_y, data_vals), (meta[0], meta[3])

