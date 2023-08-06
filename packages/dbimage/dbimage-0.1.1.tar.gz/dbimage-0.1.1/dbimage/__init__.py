import sys
import struct
import logging

import blosc
import numpy as np



DTYPE_CODE_LOOKUP = {
    np.dtype('uint8'): 0,
    np.dtype('uint16'): 1,
    np.dtype('uint32'): 2,
    np.dtype('float32'): 3

}

DTYPE_REVERSE_LOOKUP = {
    0: np.dtype('uint8'),
    1: np.dtype('uint16'),
    2: np.dtype('uint32'),
    3: np.dtype('float32'),
}

HDR_FORMAT = "iQQ" + "LLL" + "LLL"


def array_info_from_array(array):

    strides = array.__array_interface__['strides']
    if strides is None:
        strides = 0, 0, 0

    array_info = dict(
        dtype=array.dtype,
        size=array.size,
        strides=strides,
        dim=array.shape
    )

    return array_info


def array_info_to_hdr_values(array_info):

    dtype = array_info['dtype']
    try:
        dtype_code = DTYPE_CODE_LOOKUP[dtype]
    except KeyError:
        print(f"Can't handle type {dtype}")
        sys.exit(2)

    hdr_szinfo = (dtype_code, array_info['size'], array_info['packed_size'])
    hdr_values = hdr_szinfo + array_info['dim'] + array_info['strides']

    return hdr_values


def header_bytes_from_array(array, cbytes):

    array_info = array_info_from_array(array)
    array_info['packed_size'] = len(cbytes)
    logging.debug(f"Packing with array_info={array_info}")

    hdr_values = array_info_to_hdr_values(array_info)
    logging.debug(f"Packing header values {hdr_values}")
    hdr_packed = struct.pack(HDR_FORMAT, *hdr_values)

    return hdr_packed


def bytes_to_array_info(hdr_bytes):
    hdr_values = struct.unpack(HDR_FORMAT, hdr_bytes)
    logging.debug(f"Read header values: {hdr_values}")

    dtype_code, size, packed_size, *rest = hdr_values
    rdim, cdim, zdim, *strides = rest


    array_info = dict(
        dtype=DTYPE_REVERSE_LOOKUP[dtype_code],
        size=size,
        packed_size=packed_size,
        dim=(rdim, cdim, zdim),
        strides=tuple(strides)
    )

    return array_info


def arraydata_to_compressed_bytes(arraydata):

    cbytes = blosc.compress_ptr(
        arraydata.__array_interface__['data'][0],
        arraydata.size,
        arraydata.dtype.itemsize,
        cname='zlib',
        shuffle=blosc.SHUFFLE
    )

    return cbytes


def compressed_bytes_to_arraydata(cbytes, size, dtype):

    arraydata = np.empty(size, dtype=dtype)
    blosc.decompress_ptr(cbytes, arraydata.__array_interface__['data'][0])

    return arraydata


def compressed_bytes_to_shaped_array(cbytes, array_info):

    size = array_info['size']
    dtype = array_info['dtype']
    arraydata = compressed_bytes_to_arraydata(cbytes, size, dtype)

    strides = array_info['strides']
    dim = array_info['dim']
    if strides == (0, 0, 0):
        shaped_array = np.reshape(arraydata, dim)
    else:
        shaped_array = np.lib.stride_tricks.as_strided(arraydata, dim, strides, writeable=False)

    return shaped_array


