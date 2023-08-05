#!/usr/bin/env python3

import asyncio
import json

import numpy as np
import pandas as pd
from pandas.api import types as pdtypes

from gv_utils.enums import Message, MessageData, MessageFormat, MessageType


async def encode(message: dict) -> dict:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, _encode, message)


def _encode(message: dict) -> dict:
    dataformat = message[Message.format]
    if dataformat == MessageFormat.json:
        message[Message.data] = json.dumps(message[Message.data])
    elif dataformat == MessageFormat.pandas:
        message[Message.data] = _encode_pandas(message[Message.data])
    return message


def _encode_pandas(data: pd.DataFrame) -> str:
    data.fillna(MessageData.nan, inplace=True)
    for col in data.columns:
        try:
            if pdtypes.is_numeric_dtype(data[col]):
                data[col] = data[col].astype('int')
            else:
                data[col] = data[col].map(__dump_json)
        except:
            pass
    data.replace(MessageData.nan, '', inplace=True)
    return data.to_csv(sep=MessageData.csvseparator)


def __dump_json(val: object) -> str:
    string = val
    try:
        string = json.dumps(val)
    except:
        pass
    return string


async def decode(message: dict) -> dict:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, sync_decode, message)


def sync_decode(message: dict) -> dict:
    dataformat = message[Message.format]
    if dataformat == MessageFormat.json:
        message[Message.data] = json.loads(message[Message.data])
    elif dataformat == MessageFormat.pandas:
        message[Message.data] = _decode_pandas(message[Message.data])
    message[Message.type] = __remove_past_prefix_from_type(message[Message.type])
    return message


def _decode_pandas(data: str) -> pd.DataFrame:
    dataframe = pd.read_csv(data, sep=MessageData.csvseparator, index_col=0)
    for col in dataframe.columns:
        try:
            if not pdtypes.is_numeric_dtype(dataframe[col]):
                dataframe[col] = dataframe[col].map(__load_json)
        except:
            pass
    dataframe.replace(MessageData.nan, np.NaN, inplace=True)
    dataframe.replace(str(MessageData.nan), np.NaN, inplace=True)
    try:
        dataframe.index = dataframe.index.astype('str')
    except:
        pass
    return dataframe


def __load_json(string: str) -> object:
    val = string
    try:
        val = json.loads(string.replace('\'', '"'))
    except:
        pass
    return val


def __remove_past_prefix_from_type(datatype: str) -> str:
    sep = MessageType.separator
    splited = datatype.split(sep)
    return datatype if splited[0] != MessageType.past else sep.join(splited[1:])
