# -*- coding: utf-8 -*-
# generic rest http response parser interface
import itertools
import json
import logging
from abc import ABC
from aiohttp.typedefs import CIMultiDictProxy


class RestfulParser(ABC):

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

    @classmethod
    def default_result(cls) -> dict:
        return {}

    @classmethod
    def do_parse(cls, status: int, headers: CIMultiDictProxy[str], body: str, payload: dict) -> dict:
        return cls.default_result()

    @classmethod
    def parse(cls, status: int, headers: CIMultiDictProxy[str], body: str, payload: dict) -> dict:
        if 'content-type' in headers:
            supported_content_types = cls.content_type_supported() + [
                f'{t}; charset={c}' for c, t in itertools.product(cls.charset_supported(), cls.content_type_supported())
            ]
            if headers['content-type'] not in supported_content_types:
                logging.warning(f'Content-Type {headers["content-type"]} not supported by {cls.name()}')
                return cls.default_result()
        return cls.do_parse(status, headers, body, payload)


class RestfulJSONParser(RestfulParser):

    @classmethod
    def content_type_supported(cls) -> list:
        return ['application/json', 'multipart/json']

    @classmethod
    def charset_supported(cls) -> list:
        return ['utf-8']

    @classmethod
    def parse_response(cls, status: int, headers: CIMultiDictProxy[str], json_body: dict, payload: dict) -> dict:
        return cls.default_result()

    @classmethod
    def do_parse(cls, status: int, headers: CIMultiDictProxy[str], body: str, payload: dict) -> dict:
        try:
            json_body = json.loads(body, strict=False)
            return cls.parse_response(status, headers, json_body, payload)
        except json.JSONDecodeError:
            if 'verbose' in payload and payload['verbose']:
                logging.debug(f'Failed to decode JSON: {repr(body)}')
            return cls.default_result()
