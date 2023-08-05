#!/usr/bin/env python3

import aiohttp

from gv_utils import parser
from gv_utils.datetime import datetime, encode_datetime
from gv_utils.enums import MessageType, RequestParam
from gv_utils.geometry import encode_geometry, GeomType
from gv_utils.logger import Logger


class Requests:
    gvapiurl = 'http://gtlville-interface.inrialpes.fr/api'

    def __init__(self, logger: Logger):
        self.logger = logger
        self.session = aiohttp.ClientSession()

    async def get_data_point(self, datapointeids: list = None, datatypeeids: list = None,
                             area: GeomType = None) -> dict:
        params = {}
        if datatypeeids is not None:
            params[RequestParam.datatypeeid] = datatypeeids  # TODO: is encoding necessary?
        return await self._get_location(datapointeids, area, MessageType.road, params)

    async def get_road(self, roadeids: list = None, area: GeomType = None) -> dict:
        return await self._get_location(roadeids, area, MessageType.road)

    async def get_zone_point(self, zoneeids: list = None, area: GeomType = None) -> dict:
        return await self._get_location(zoneeids, area, MessageType.zone)

    async def _get_location(self, eids: list, area: GeomType, applyto: str, params: dict = None) -> dict:
        if params is None:
            params = {}

        if eids is not None:
            params[RequestParam.eid] = eids  # TODO: is encoding necessary?
        if area is not None:
            params[RequestParam.area] = encode_geometry(area)
        return await self._get('{}/{}'.format(MessageType.location, applyto), params)

    async def get_road_data_point(self, area: GeomType = None) -> dict:
        params = {}
        if area is not None:
            params[RequestParam.area] = encode_geometry(area)
        return await self._get('{}/{}/{}'.format(MessageType.mapping, MessageType.road, MessageType.datapoint), params)

    async def get_data_point_data_quality(self, period: str, fromdatetime: datetime, datapointeids: list = None,
                                          datatypeeids: list = None, todatetime: datetime = None) -> dict:
        params = {}
        if datatypeeids is not None:
            params[RequestParam.datatypeeid] = datatypeeids  # TODO: is encoding necessary?
        return await self._get_data_quality(period, fromdatetime, datapointeids, todatetime, MessageType.datapoint,
                                            params)

    async def get_data_type_data_quality(self, period: str, fromdatetime: datetime, datatypeeids: list = None,
                                         todatetime: datetime = None) -> dict:
        return await self._get_data_quality(period, fromdatetime, datatypeeids, todatetime, MessageType.datatype)

    async def get_road_data_quality(self, period: str, fromdatetime: datetime, roadeids: list = None,
                                    todatetime: datetime = None) -> dict:
        return await self._get_data_quality(period, fromdatetime, roadeids, todatetime, MessageType.road)

    async def _get_data_quality(self, period: str, fromdatetime: datetime, locationeids: list, todatetime: datetime,
                                applyto: str, params: dict = None) -> dict:
        return await self.__get_data(period, fromdatetime, locationeids, todatetime,
                                     '{}/{}'.format(MessageType.dataquality, applyto), params)

    async def get_data_point_indicator(self, indicator: str, period: str, fromdatetime: datetime,
                                       datapointeids: list = None, datatypeeids: list = None,
                                       todatetime: datetime = None) -> dict:
        params = {}
        if datatypeeids is not None:
            params[RequestParam.datatypeeid] = datatypeeids  # TODO: is encoding necessary?
        return await self._get_indicator(indicator, period, fromdatetime, datapointeids, todatetime,
                                         MessageType.datapoint, params)

    async def get_data_point_imputed_indicator(self, indicator: str, period: str, fromdatetime: datetime,
                                               datapointeids: list = None, datatypeeids: list = None,
                                               todatetime: datetime = None) -> dict:
        params = {}
        if datatypeeids is not None:
            params[RequestParam.datatypeeid] = datatypeeids  # TODO: is encoding necessary?
        return await self._get_indicator(indicator, period, fromdatetime, datapointeids, todatetime,
                                         '{}/{}'.format(MessageType.imputed, MessageType.datapoint), params)

    async def get_road_indicator(self, indicator: str, period: str, fromdatetime: datetime, roadeids: list = None,
                                 todatetime: datetime = None) -> dict:
        return await self._get_indicator(indicator, period, fromdatetime, roadeids, todatetime, MessageType.road)

    async def _get_indicator(self, indicator: str, period: str, fromdatetime: datetime, locationeids: list,
                             todatetime: datetime, applyto: str, params: dict = None) -> dict:
        if params is None:
            params = {}

        params[RequestParam.indicator] = indicator
        return await self.__get_data(period, fromdatetime, locationeids, todatetime,
                                     '{}/{}'.format(MessageType.indicator, applyto), params)

    async def __get_data(self, period: str, fromdatetime: datetime, locationeids: list, todatetime: datetime,
                         applyto: str, params) -> dict:
        if params is None:
            params = {}

        params[RequestParam.period] = period
        params[RequestParam.fromdatetime] = encode_datetime(fromdatetime)
        if locationeids is not None:
            params[RequestParam.eid] = locationeids  # TODO: is encoding necessary?
        if todatetime is not None:
            params[RequestParam.todatetime] = encode_datetime(todatetime)
        return await self._get(applyto, params)

    async def get_zone_travel_time(self, frompointeid: str, topointeid: str, period: str, fromdatetime: datetime,
                                   todatetime: datetime = None) -> dict:
        params = {
            RequestParam.frompointeid: frompointeid,
            RequestParam.topointeid: topointeid,
            RequestParam.period: period,
            RequestParam.fromdatetime: encode_datetime(fromdatetime)
        }
        if todatetime is not None:
            params[RequestParam.todatetime] = encode_datetime(todatetime)
        return await self._get('{}/{}'.format(MessageType.traveltime, MessageType.zone), params)

    async def _get(self, suffix: str, params: dict = None) -> dict:
        message = {}
        async with self.session.get('{}/{}'.format(self.gvapiurl, suffix), params=params) as resp:
            if resp.status == 200:
                message = await parser.decode(await resp.json())
        return message

    async def close(self) -> None:
        await self.session.close()
