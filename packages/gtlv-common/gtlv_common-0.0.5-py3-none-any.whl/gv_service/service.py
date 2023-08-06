#!/usr/bin/env python3

import asyncio
import time
from typing import Awaitable, Callable

from gv_pubsub.pubsub import PubSub
from gv_requests.requests import Requests
from gv_utils.asyncio import check_event_loop
from gv_utils.datetime import datetime
from gv_utils.enums import MessageKind, AttId
from gv_utils.geometry import BaseGeometry
from gv_utils.logger import Logger


class Service:
    samplings = {MessageKind.karrusrd: 1 * 60, MessageKind.metropme: 1 * 60, MessageKind.tomtomfcd: 1 * 60}

    def __init__(self, logger: Logger, futures: list = None, callbacks: dict = None,
                 custom_data_decoder: Callable = None) -> None:
        if futures is None:
            futures = []
        if callbacks is None:
            callbacks = {}

        self.logger = logger
        self.futures = futures
        self.callbacks = callbacks
        self.pubsub = PubSub(self.logger, custom_data_decoder)
        self.requests = Requests(logger)
        self._mainfut = None

    async def async_init(self) -> None:
        pass

    def start(self, redisaddr: str) -> None:
        check_event_loop()  # will create a new event loop if needed (if we are not in the main thread)
        self.logger.info('RPC client is starting.')
        try:
            asyncio.run(self._run(redisaddr))
        except KeyboardInterrupt:
            pass
        self.logger.info('RPC client has stopped.')

    async def _run(self, redisaddr: str) -> None:
        try:
            await self.pubsub.async_init(redisaddr)
            await self.async_init()
            self.logger.info('RPC client has started.')
            running = True
            while running:
                try:
                    self._mainfut = asyncio.gather(
                        *self.futures,
                        *[self._subscribe(datakind, callback) for datakind, callback in self.callbacks.items()]
                    )
                    await self._mainfut
                except KeyboardInterrupt:
                    self._cancel()
                    running = False
                except:
                    time.sleep(1)
                else:
                    running = False
            await self._close()
        except:
            import traceback
            traceback.print_exc()
            await self._close()

    async def _close(self) -> None:
        await asyncio.gather(self.pubsub.close(), self.requests.close())

    def _cancel(self) -> None:
        if self._mainfut is not None:
            self._mainfut.cancel()
            self._mainfut = None

    async def _publish(self, data: object, dataformat: str, datatimestamp, datakind: str) -> bool:
        return await self.pubsub.publish(data, dataformat, datatimestamp, datakind)

    async def _subscribe(self, datakind: str, callback: Callable[[dict], Awaitable]) -> None:
        await self.pubsub.subscribe(datakind, callback)

    async def _get_data_point(self, datapointeids: list = None, datatypeeids: list = None,
                              area: BaseGeometry = None) -> dict:
        return await self.requests.get_data_point(datapointeids, datatypeeids, area)

    async def _get_road(self, roadeids: list = None, area: BaseGeometry = None) -> dict:
        return await self.requests.get_road(roadeids, area)

    async def _get_zone_point(self, zoneeids: list = None, area: BaseGeometry = None) -> dict:
        return await self.requests.get_zone_point(zoneeids, area)

    async def _get_road_data_point(self, area: BaseGeometry = None) -> dict:
        return await self.requests.get_road_data_point(area)

    async def _get_data_point_data_quality(self, period: str, fromdatetime: datetime, datapointeids: list = None,
                                           datatypeeids: list = None, todatetime: datetime = None) -> dict:
        return await self.requests.get_data_point_data_quality(period, fromdatetime, datapointeids, datatypeeids,
                                                               todatetime)

    async def _get_data_type_data_quality(self, period: str, fromdatetime: datetime, datatypeeids: list = None,
                                          todatetime: datetime = None) -> dict:
        return await self.requests.get_data_type_data_quality(period, fromdatetime, datatypeeids, todatetime)

    async def _get_road_data_quality(self, period: str, fromdatetime: datetime, roadeids: list = None,
                                     todatetime: datetime = None) -> dict:
        return await self.requests.get_road_data_quality(period, fromdatetime, roadeids, todatetime)

    async def _get_data_point_indicator(self, indicator: str, period: str, fromdatetime: datetime,
                                        datapointeids: list = None, datatypeeids: list = None,
                                        todatetime: datetime = None) -> dict:
        return await self.requests.get_data_point_indicator(indicator, period, fromdatetime, datapointeids,
                                                            datatypeeids, todatetime)

    async def _get_data_point_imputed_indicator(self, indicator: str, period: str, fromdatetime: datetime,
                                                datapointeids: list = None, datatypeeids: list = None,
                                                todatetime: datetime = None) -> dict:
        return await self.requests.get_data_point_imputed_indicator(indicator, period, fromdatetime, datapointeids,
                                                                    datatypeeids, todatetime)

    async def _get_road_indicator(self, indicator: str, period: str, fromdatetime: datetime, roadeids: list = None,
                                  todatetime: datetime = None) -> dict:
        return await self.requests.get_road_indicator(indicator, period, fromdatetime, roadeids, todatetime)

    async def _get_zone_travel_time(self, frompointeid: str, topointeid: str, period: str, fromdatetime: datetime,
                                    todatetime: datetime = None) -> dict:
        return await self.requests.get_zone_travel_time(frompointeid, topointeid, period, fromdatetime, todatetime)

    @staticmethod
    def _get_data_type_eid_from_data_points(datapoints: dict) -> str:
        datapointeid, datapoint = datapoints.popitem()
        datatypeeid = datapoint[AttId.datatypeeid]
        datapoints[datapointeid] = datapoint
        return datatypeeid


def start(Application, threaded=False):
    if threaded:
        import threading
        threading.Thread(target=start, args=(Application, False), daemon=True).start()
        print('Starting application in a background thread...')
    else:
        Application()
