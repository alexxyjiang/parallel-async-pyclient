# -*- coding: utf-8 -*-
# generic rest http asyncio client based on aiohttp
from aiohttp import ClientSession
from .parser import RestfulParser


class RestfulClient(object):

    def __init__(self, client_session: ClientSession, client_parser: RestfulParser):
        self.__client_session__ = client_session
        self.__client_parser__ = client_parser

    async def request_parse(self, method: str, url: str, **kwargs) -> dict:
        async with self.__client_session__.request(method, url, **kwargs) as response:
            status = response.status
            headers = response.headers
            body = await response.text()
            if status in self.__client_parser__.support_status():
                return self.__client_parser__.parse(status, headers, body)
