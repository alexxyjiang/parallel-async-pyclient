# -*- coding: utf-8 -*-
# model of json request decorators
from abc import ABC, abstractmethod
from .request import JsonRequest


class JsonRequestDecorator(JsonRequest, ABC):

    def __init__(self, json_request: JsonRequest):
        self.__inner_request__ = json_request

    @abstractmethod
    def get_json_object(self) -> dict:
        pass

    @abstractmethod
    def to_plain_text(self) -> str:
        pass
