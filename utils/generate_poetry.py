# -*- coding: utf-8 -*-

from utils.mysql import OperationMysql

"""
功能 ： 用于 获取可用诗词

developer ： 刘嘉林

"""


def read_data():
    oper = OperationMysql()
    text = oper.search_one("select id,content from poetry where used = '0' and status = '0'")
    id = text["id"]
    oper.updata_one("UPDATE poetry SET used = 1 WHERE id = '" + str(id) + "';")
    content = text["content"]

    return id, content


def generate_poetry():
    id, content = read_data()
    json_ = {
        'id': id,
        'content': content
    }
    return json_


if __name__ == '__main__':
    generate_poetry()
