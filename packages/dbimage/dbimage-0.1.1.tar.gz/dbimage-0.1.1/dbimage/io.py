import struct

import numpy as np

from dbimage import (
    HDR_FORMAT,
    bytes_to_array_info,
    compressed_bytes_to_shaped_array,
    arraydata_to_compressed_bytes,
    header_bytes_from_array
)


def read_array_info_from_fpath(fpath):

    with open(fpath, "rb") as fh:
        hdr_bytes = fh.read(struct.calcsize(HDR_FORMAT))

    array_info = bytes_to_array_info(hdr_bytes)

    return array_info


def read_dbim_from_fpath(fpath):

    with open(fpath, 'rb') as fh:
        hdr_bytes = fh.read(struct.calcsize(HDR_FORMAT))
        array_info = bytes_to_array_info(hdr_bytes)
        packed_size = array_info['packed_size']
        fh.seek(-packed_size, 2)
        cbytes = fh.read()

    shaped_array = compressed_bytes_to_shaped_array(cbytes, array_info)

    return shaped_array


def write_array_to_fpath(fpath, array):

    cbytes = arraydata_to_compressed_bytes(array)
    hdr_bytes = header_bytes_from_array(array, cbytes)

    with open(fpath, 'wb') as fh:
        fh.write(hdr_bytes)
        fh.write(cbytes)
