# -*- coding: utf-8 -*-
# generic rest http response parser interface
import itertools
import json
import logging
from abc import ABC, abstractmethod
from aiohttp.typedefs import CIMultiDictProxy


class RestfulParser(ABC):

    @abstractmethod
    def __init__(self, **kwargs):
        pass

    @classmethod
    def name(cls) -> str:
        return cls.__name__

    @classmethod
    def status_supported(cls) -> list:
        return [200]

    @classmethod
    def content_type_supported(cls) -> list:
        return []

    @classmethod
    def charset_supported(cls) -> list:
        return []

    @abstractmethod
    def update_by_status(self, status: int, **kwargs):
        pass

    @abstractmethod
    def update_by_headers(self, headers: CIMultiDictProxy[str], **kwargs):
        pass

    @abstractmethod
    def parse_body(self, body: str, **kwargs) -> dict:
        return {}

    def parse(self, status: int, headers: CIMultiDictProxy[str], body: str, **kwargs) -> dict:
        self.update_by_status(status)
        self.update_by_headers(headers)
        if 'content-type' not in headers:
            return self.parse_body(body, **kwargs)
        else:
            supported_content_types = self.content_type_supported() + [
                f'{t}; charset={c}' for c, t in itertools.product(self.charset_supported(), self.content_type_supported())
            ]
            if headers['content-type'] in supported_content_types:
                return self.parse_body(body, **kwargs)
            else:
                logging.warning(f'Content-Type {headers["content-type"]} not supported by {self.name()}')
                raise NotImplementedError(f"Content-Type {headers['content-type']} not supported by {self.name()}")


class RestfulJSONParser(RestfulParser):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__result__ = {}

    @classmethod
    def content_type_supported(cls) -> list:
        return ['application/json', 'multipart/json']

    @classmethod
    def charset_supported(cls) -> list:
        return ['utf-8']

    @abstractmethod
    def parse_response(self, **kwargs) -> dict:
        return {}

    def update_by_status(self, status: int, **kwargs):
        self.__result__['status'] = status

    def update_by_headers(self, headers: CIMultiDictProxy[str], **kwargs):
        self.__result__['headers'] = headers

    def parse_body(self, body: str, **kwargs) -> dict:
        try:
            self.__result__['json_response'] = json.loads(body)
            return self.parse_response(**kwargs)
        except json.JSONDecodeError:
            logging.warning(f'Failed to decode JSON: {body}')
            return {}
