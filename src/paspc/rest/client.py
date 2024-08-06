# -*- coding: utf-8 -*-
# generic rest http asyncio client based on aiohttp
import logging
from typing import Any
from aiohttp import ClientSession
from .parser import RestfulParser


class RestfulClient(object):

    def __init__(self, client_session: ClientSession, client_parser: RestfulParser):
        self.__client_session__ = client_session
        self.__client_parser__ = client_parser

    async def request_parse(self, method: str, url: str, payload: Any, **kwargs) -> dict:
        async with self.__client_session__.request(method, url, **kwargs) as response:
            status = response.status
            headers = response.headers
            body = await response.text()
            if status in self.__client_parser__.status_supported():
                return self.__client_parser__.parse(status, headers, body, payload)
            else:
                logging.warning(f'Status {status} not supported by {self.__client_parser__.name()}')
                raise NotImplementedError(f"Status {status} not supported by {self.__client_parser__.name()}")
