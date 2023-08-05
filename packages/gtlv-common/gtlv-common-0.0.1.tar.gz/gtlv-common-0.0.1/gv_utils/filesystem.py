#!/usr/bin/env python3

import os

import aiofiles

from gv_utils import datetime


DATA_PATH_STRUCT = '%Y/%m/%d/'


async def write_data(basepath: str, datafilestruct: str, data: bytes, datatype: str, datadate: str) -> str:
    fullpath = os.path.join(_get_path(basepath, datatype, datadate), _get_file_name(datadate, datafilestruct))
    await _write_bytes(fullpath, data)
    return fullpath


async def read_data(basepath: str, datafilestruct: str, datatype: str, datadate: str) -> bytes:
    return await _read_bytes(_get_file_path(basepath, datafilestruct, datatype, datadate))


async def data_exists(basepath: str, datafilestruct: str, datatype: str, datadate: str) -> bool:
    return os.path.exists(_get_file_path(basepath, datafilestruct, datatype, datadate))


def _get_path(basepath: str, datatype: str, datadate: str) -> str:
    return mkdir_if_not_exist(os.path.join(basepath, _get_datatype_dir(datatype),
                                           datetime.encode_datetime(datadate, DATA_PATH_STRUCT)))


def _get_file_name(datadate: datetime, datafilestruct: str) -> str:
    return datetime.encode_datetime(datadate, datafilestruct)


def _get_datatype_dir(datatype: str) -> str:
    return datatype.upper()


def _get_file_path(basepath: str, datafilestruct: str, datatype: str, datadate: datetime) -> str:
    return os.path.join(basepath,
                        _get_datatype_dir(datatype),
                        datetime.encode_datetime(datadate, DATA_PATH_STRUCT + datafilestruct))


async def _write_bytes(path: str, b: bytes) -> None:
    async with aiofiles.open(path, 'wb') as file:
        await file.write(b)


async def _read_bytes(path: str) -> bytes:
    if os.path.exists(path):
        async with aiofiles.open(path, 'rb') as file:
            b = await file.read()
    else:
        b = b''
    return b


def join_if_not_abs(root: str, path: str) -> str:
    if not os.path.isabs(path):
        path = os.path.join(root, path)
    return path


def mkdir_if_not_exist(path: str) -> str:
    if not os.path.exists(path):
        os.makedirs(path)
    return path
