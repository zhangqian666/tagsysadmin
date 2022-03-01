# -*- coding: utf-8 -*-

from utils.mysql import OperationMysql
import json

"""
功能 ： 用于 收集完报表后 提交 最终数据

developer ： 雷艳

"""


class MysqlManager:
    @staticmethod
    def save_data(id, tag_user, taged_data):
        mysql = OperationMysql()
        mysql.updata_one("update poetry set tag_by='{name}', tag_end='{data}', status=1 where id = {id}".format(
            name=tag_user, data=json.dumps(taged_data, ensure_ascii=False), id=id))
        return "ok"
