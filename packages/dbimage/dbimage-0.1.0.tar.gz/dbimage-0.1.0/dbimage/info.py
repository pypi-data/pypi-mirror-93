import logging

import click

from dbimage.io import read_array_info_from_fpath, read_dbim_from_fpath


@click.command()
@click.argument('dbim_fpath')
def dbim_info(dbim_fpath):

    logging.basicConfig(level=logging.DEBUG)

    array_info = read_array_info_from_fpath(dbim_fpath)
    print(array_info)
    # print(f"Read array with shape {sa.shape}, dtype {sa.dtype}")
