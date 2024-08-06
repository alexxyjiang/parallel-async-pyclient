# -*- coding: utf-8 -*-
# generic rest http response parser interface
import itertools
import json
import logging
from abc import ABC, abstractmethod
from typing import Any
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
    def do_parse(self, status: int, headers: CIMultiDictProxy[str], body: str, payload: Any) -> dict:
        return {}

    def parse(self, status: int, headers: CIMultiDictProxy[str], body: str, payload: Any) -> dict:
        if 'content-type' not in headers:
            return self.do_parse(status, headers, body, payload)
        else:
            supported_content_types = self.content_type_supported() + [
                f'{t}; charset={c}' for c, t in itertools.product(self.charset_supported(), self.content_type_supported())
            ]
            if headers['content-type'] in supported_content_types:
                return self.do_parse(status, headers, body, payload)
            else:
                logging.warning(f'Content-Type {headers["content-type"]} not supported by {self.name()}')
                raise NotImplementedError(f"Content-Type {headers['content-type']} not supported by {self.name()}")


class RestfulJSONParser(RestfulParser):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def content_type_supported(cls) -> list:
        return ['application/json', 'multipart/json']

    @classmethod
    def charset_supported(cls) -> list:
        return ['utf-8']

    @abstractmethod
    def parse_response(self, status: int, headers: CIMultiDictProxy[str], json_body: Any, payload: Any) -> dict:
        return {}

    def do_parse(self, status: int, headers: CIMultiDictProxy[str], body: str, payload: Any) -> dict:
        try:
            json_body = json.loads(body)
            return self.parse_response(status, headers, json_body, payload)
        except json.JSONDecodeError:
            logging.warning(f'Failed to decode JSON: {body}')
            return {}
