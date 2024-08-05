# -*- coding: utf-8 -*-
# generic rest http response parser interface
import itertools
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
    def support_status(cls) -> list:
        return [200]

    @classmethod
    def support_parse_headers(cls) -> bool:
        return False

    @classmethod
    def support_content_type(cls) -> list:
        return []

    @classmethod
    def support_charset(cls) -> list:
        return ['utf-8']

    @abstractmethod
    def update_by_status(self, status: int):
        pass

    @abstractmethod
    def update_by_headers(self, headers: CIMultiDictProxy[str]):
        pass

    @abstractmethod
    def parse_body(self, body: str, **kwargs) -> dict:
        return {}

    def parse(self, status: int, headers: CIMultiDictProxy[str], body: str, **kwargs) -> dict:
        self.update_by_status(status)
        if self.support_parse_headers():
            self.update_by_headers(headers)
        if 'content-type' not in headers:
            return self.parse_body(body, **kwargs)
        else:
            supported_content_types = self.support_content_type() + [
                f'{t}; charset={c}' for c, t in itertools.product(self.support_charset(), self.support_content_type())
            ]
            if headers['content-type'] in supported_content_types:
                return self.parse_body(body, **kwargs)
            else:
                return {}
