# -*- coding: utf-8 -*-
# unit test for config

import unittest

from src.paspc import GenericYamlConfig


class TestGenericYamlConfig(unittest.TestCase):

    def test_io(self):
        config = GenericYamlConfig()
        config_dict = config.load_config('config.yaml')
        self.assertEqual({'major': {'minor': {'float': 1.024, 'int': -2, 'list': [2, 1, 3], 'str': '2024'}}}, config_dict)
        config.dump_config('dump.yaml')
        config.load_config('dump.yaml')
        self.assertEqual(config_dict, config.get_config())
        print(config_dict)
        print(config.get_config())


if __name__ == '__main__':
    unittest.main()
