# -*- coding: utf-8 -*-
# model of json request
import json
from abc import ABC, abstractmethod


class JsonRequest(ABC):

    @abstractmethod
    def get_json_object(self) -> dict:
        pass

    @abstractmethod
    def to_plain_text(self) -> str:
        pass


class BasicJsonRequest(JsonRequest):

    def __init__(self, plain_text: str):
        self.__inner_object__ = json.loads(plain_text)

    def get_json_object(self) -> dict:
        return self.__inner_object__

    def to_plain_text(self) -> str:
        return json.dumps(self.__inner_object__, ensure_ascii=False, indent=2)
