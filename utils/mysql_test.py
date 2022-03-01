# -*- coding: utf-8 -*-

"""
@author: zhangqian

@contact: 

@Created on: 2021-04-08 14:14
"""

from utils.mysql import OperationMysql

mysql = OperationMysql()
# mysql.insert_one("insert into poetry (content,status) values ('《红楼梦》中袭人的名字源自陆游的一句诗，请问这句诗是什么？',0)")

all_data = mysql.search_all("select * from poetry limit 10")

print(all_data)
