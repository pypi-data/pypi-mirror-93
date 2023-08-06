#!/usr/bin/env python3

import aiohttp

from gv_utils import parser
from gv_utils.datetime import datetime, to_str
from gv_utils.enums import RequestParam, RequestPath
from gv_utils.geometry import BaseGeometry, encode_geometry
from gv_utils.logger import Logger


class Requests:
    gvapiurl = 'http://gtlville-interface.inrialpes.fr/api'

    def __init__(self, logger: Logger) -> None:
        self.logger = logger
        self.session = aiohttp.ClientSession()

    async def get_data_point(self, datapointeids: list = None, datatypeeids: list = None,
                             area: BaseGeometry = None) -> dict:
        params = {}
        if datatypeeids is not None:
            params[RequestParam.datatype] = self.__encode_list_params(datatypeeids)
        return await self._get_location(datapointeids, area, RequestPath.datapoint, params)

    async def get_road(self, roadeids: list = None, area: BaseGeometry = None) -> dict:
        return await self._get_location(roadeids, area, RequestPath.road)

    async def get_zone_point(self, zoneeids: list = None, area: BaseGeometry = None) -> dict:
        return await self._get_location(zoneeids, area, RequestPath.zone)

    async def _get_location(self, eids: list, area: BaseGeometry, applyto: str, params: dict = None) -> dict:
        if params is None:
            params = {}

        if eids is not None:
            params[RequestParam.eid] = self.__encode_list_params(eids)
        if area is not None:
            params[RequestParam.within] = encode_geometry(area)
        return await self._get('{}/{}'.format(RequestPath.location, applyto), params)

    async def get_road_data_point(self, area: BaseGeometry = None) -> dict:
        params = {}
        if area is not None:
            params[RequestParam.within] = encode_geometry(area)
        return await self._get('{}/{}/{}'.format(RequestPath.mapping, RequestPath.road, RequestPath.datapoint), params)

    async def get_data_point_data_quality(self, period: str, fromdatetime: datetime, datapointeids: list = None,
                                          datatypeeids: list = None, todatetime: datetime = None) -> dict:
        params = {}
        if datatypeeids is not None:
            params[RequestParam.datatype] = self.__encode_list_params(datatypeeids)
        return await self._get_data_quality(period, fromdatetime, datapointeids, todatetime, RequestPath.datapoint,
                                            params)

    async def get_data_type_data_quality(self, period: str, fromdatetime: datetime, datatypeeids: list = None,
                                         todatetime: datetime = None) -> dict:
        return await self._get_data_quality(period, fromdatetime, datatypeeids, todatetime, RequestPath.datatype)

    async def get_road_data_quality(self, period: str, fromdatetime: datetime, roadeids: list = None,
                                    todatetime: datetime = None) -> dict:
        return await self._get_data_quality(period, fromdatetime, roadeids, todatetime, RequestPath.road)

    async def _get_data_quality(self, period: str, fromdatetime: datetime, locationeids: list, todatetime: datetime,
                                applyto: str, params: dict = None) -> dict:
        return await self.__get_data(period, fromdatetime, locationeids, todatetime,
                                     '{}/{}'.format(RequestPath.dataquality, applyto), params)

    async def get_data_point_indicator(self, indicator: str, period: str, fromdatetime: datetime,
                                       datapointeids: list = None, datatypeeids: list = None,
                                       todatetime: datetime = None) -> dict:
        params = {}
        if datatypeeids is not None:
            params[RequestParam.datatype] = self.__encode_list_params(datatypeeids)
        return await self._get_indicator(indicator, period, fromdatetime, datapointeids, todatetime,
                                         RequestPath.datapoint, params)

    async def get_data_point_imputed_indicator(self, indicator: str, period: str, fromdatetime: datetime,
                                               datapointeids: list = None, datatypeeids: list = None,
                                               todatetime: datetime = None) -> dict:
        params = {}
        if datatypeeids is not None:
            params[RequestParam.datatype] = self.__encode_list_params(datatypeeids)
        return await self._get_indicator(indicator, period, fromdatetime, datapointeids, todatetime,
                                         '{}/{}'.format(RequestPath.imputed, RequestPath.datapoint), params)

    async def get_road_indicator(self, indicator: str, period: str, fromdatetime: datetime, roadeids: list = None,
                                 todatetime: datetime = None) -> dict:
        return await self._get_indicator(indicator, period, fromdatetime, roadeids, todatetime, RequestPath.road)

    async def _get_indicator(self, indicator: str, period: str, fromdatetime: datetime, locationeids: list,
                             todatetime: datetime, applyto: str, params: dict = None) -> dict:
        if params is None:
            params = {}

        params[RequestParam.indicator] = indicator
        return await self.__get_data(period, fromdatetime, locationeids, todatetime,
                                     '{}/{}'.format(RequestPath.indicator, applyto), params)

    async def __get_data(self, period: str, fromdatetime: datetime, locationeids: list, todatetime: datetime,
                         applyto: str, params) -> dict:
        if params is None:
            params = {}

        params[RequestParam.period] = period
        params[RequestParam.fromdatetime] = to_str(fromdatetime)
        if locationeids is not None:
            params[RequestParam.eid] = self.__encode_list_params(locationeids)
        if todatetime is not None:
            params[RequestParam.todatetime] = to_str(todatetime)
        return await self._get(applyto, params)

    async def get_zone_travel_time(self, frompointeid: str, topointeid: str, period: str, fromdatetime: datetime,
                                   todatetime: datetime = None) -> dict:
        params = {
            RequestParam.frompoint: frompointeid,
            RequestParam.topoint: topointeid,
            RequestParam.period: period,
            RequestParam.fromdatetime: to_str(fromdatetime)
        }
        if todatetime is not None:
            params[RequestParam.todatetime] = to_str(todatetime)
        return await self._get('{}/{}'.format(RequestPath.traveltime, RequestPath.zone), params)

    async def _get(self, suffix: str, params: dict = None) -> dict:
        message = {}
        async with self.session.get('{}/{}'.format(self.gvapiurl, suffix), params=params) as resp:
            if resp.status == 200:
                message = await parser.decode_message(await resp.text())
        return message

    @staticmethod
    def __encode_list_params(params: list) -> str:
        return RequestParam.separator.join(params)

    async def close(self) -> None:
        await self.session.close()
