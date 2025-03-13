# -*- coding: utf-8 -*-
# generic rest http asyncio client based on aiohttp
import logging
from aiohttp import ClientSession
from .parser import RestfulParser


class RestfulClient(object):

    def __init__(self, client_session: ClientSession, client_parser: RestfulParser):
        self.__client_session__ = client_session
        self.__client_parser__ = client_parser

    def get_parser(self) -> RestfulParser:
        return self.__client_parser__

    async def request_parse(self, method: str, url: str, payload: dict, **kwargs) -> dict:
        try:
            async with self.__client_session__.request(method, url, **kwargs) as response:
                status = response.status
                headers = response.headers
                body = await response.text()
                if 'verbose' in payload and payload['verbose']:
                    logging.debug(f'Request url {url} with payload {payload} and kwargs {kwargs}')
                if status in self.__client_parser__.status_supported():
                    return self.__client_parser__.parse(status, headers, body, payload)
                else:
                    logging.warning(f'Response of {url} with status {status} not supported by {self.__client_parser__.name()}')
                    return self.__client_parser__.default_result()
        except Exception as e:
            logging.error(f'Error occurred while requesting {url} with payload {payload} and kwargs {kwargs}: {str(e)}')
            return self.__client_parser__.default_result()
