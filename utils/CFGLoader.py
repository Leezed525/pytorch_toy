"""
-*- coding: utf-8 -*-
@Author : Leezed
@Time : 2024/3/20 20:58
"""
from utils.YamlUtil import YamlUtil
import os

current_directory_path = os.path.dirname(os.path.abspath(__file__))
configs_path = os.path.join(current_directory_path, '../../configs')


class CFGLoader(dict):
    def __getattr__(self, item):
        if item in self:
            value = self[item]
            if isinstance(value, dict):
                return CFGLoader(value)
            else:
                return value
        else:
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{item}'")

    def __setattr__(self, key, value):
        print("in set")
        print(key)
        print(value)
        print("before change :", self[key])

        self[key] = value
        print("after change :", self[key])


def get_cfg(path, cfg_name):
    return YamlUtil(path, cfg_name if cfg_name.endswith(".yml") else cfg_name + ".yml").content


def env_setting(cfg_name):
    """
    获取配置文件 ，默认是local.yaml
    :param cfg_name:  如果不想获取local.yaml，可以传入其他的配置文件名
    :return: 返回配置文件
    """
    cfg = CFGLoader(get_cfg(configs_path, cfg_name if cfg_name is not None else 'local.yml'))
    return cfg
