# -*- coding: utf-8 -*-
# generic configuration interface for parser
import yaml


class GenericYamlConfig(object):

    def __init__(self):
        self.__config__ = None

    def load_config(self, config_file: str) -> dict:
        with open(config_file, 'r') as file:
            self.__config__ = yaml.safe_load(file)
            return self.get_config()

    def dump_config(self, config_file: str):
        with open(config_file, 'w') as file:
            yaml.safe_dump(self.__config__, file)

    def get_config(self) -> dict:
        return self.__config__
