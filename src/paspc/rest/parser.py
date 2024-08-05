# -*- coding: utf-8 -*-
# generic rest http response parser interface
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
    @abstractmethod
    def support_status(cls) -> set:
        return {200}

    @classmethod
    @abstractmethod
    def support_parse_headers(cls) -> bool:
        return False

    @classmethod
    @abstractmethod
    def support_content_type(cls) -> set:
        return set()

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
        if 'content-type' in headers and headers['content-type'] in self.support_content_type():
            return self.parse_body(body, **kwargs)
        else:
            return {}
