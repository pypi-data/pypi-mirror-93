import logging

import click
import numpy as np
from tifffile import TiffFile

from dbimage.io import write_array_to_fpath


def arraydata_from_tif_fpath(tif_fpath):

    with TiffFile(tif_fpath) as tif:
        rawdata = tif.asarray()

    arraydata = np.transpose(rawdata, (1, 2, 0))

    return arraydata


@click.command()
@click.argument('input_tif_fpath')
@click.argument('output_dbim_fpath')
def convert_tif_image(input_tif_fpath, output_dbim_fpath):

    logging.basicConfig(level=logging.DEBUG)

    arraydata = arraydata_from_tif_fpath(input_tif_fpath)
    logging.info(f"Loaded TIFF with shape {arraydata.shape}, dtype {arraydata.dtype}")

    write_array_to_fpath(output_dbim_fpath, arraydata)
