# -*- coding: utf-8 -*-

"""
@author: zhangqian

@contact: 

@Created on: 2021-04-12 19:02
"""


class BaseConfig:
    DEBUG = True


class TestConfig(BaseConfig):
    NEO4J_URL = "http://39.105.121.160:27474/"
    NEO4J_USER = "neo4j"
    NEO4J_PASSWD = "123456"

    MYSQL_URL = "39.105.121.160"
    MYSQL_PORT = 23306
    MYSQL_USER = "root"
    MYSQL_PASSWD = "123456"
    MYSQL_DB = "poetry"


class ProConfig(BaseConfig):
    NEO4J_URL = "http://172.18.0.2:7474/"
    NEO4J_USER = "neo4j"
    NEO4J_PASSWD = "123456"

    MYSQL_URL = "172.18.0.3"
    MYSQL_PORT = 3306
    MYSQL_USER = "root"
    MYSQL_PASSWD = "123456"
    MYSQL_DB = "poetry"


conf = {
    "test": TestConfig,
    "pro": ProConfig
}
