#!/usr/bin/env python3

import asyncio
import traceback
from typing import Awaitable, Callable

import aioredis

from gv_utils import parser
from gv_utils.enums import Message
from gv_utils.logger import Logger


class PubSub:

    def __init__(self, logger: Logger, redisaddr: str):
        self.logger = logger
        self.redis = aioredis.create_redis_pool(redisaddr)

    async def publish(self, data: object, dataformat: str, datatimestamp, datatype: str) -> bool:
        success = False
        try:
            message = {
                Message.data: data,
                Message.format: dataformat,
                Message.timestamp: datatimestamp,
                Message.type: datatype
            }
            await self.redis.publish_json(datatype, await parser.encode(message))
            success = True
        except:
            self.logger.error(traceback.format_exc())
            self.logger.error('An error occurred while publishing {}.'.format(datatype))
        finally:
            return success

    async def subscribe(self, datatype: str, callback: Callable[[dict], Awaitable]) -> None:
        channel, = await self.redis.subscribe(datatype)
        self.logger.info('RPC client has subscribed to {}.'.format(datatype))
        while await channel.wait_message():
            self.logger.debug('New {}.'.format(datatype))
            try:
                message = await channel.get_json()
                asyncio.create_task(callback(await parser.decode(message)))
            except:
                self.logger.error(traceback.format_exc())
                self.logger.error('An error occurred while handling {}.'.format(datatype))
        self.logger.info('RPC client has unsubscribed from {}.'.format(datatype))

    async def close(self) -> None:
        if self.redis is not None:
            self.redis.close()
            await self.redis.wait_closed()
