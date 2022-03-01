# -*- coding: utf-8 -*-

"""
@author: zhangqian

@contact: 

@Created on: 2021-04-18 10:36
"""
from utils.mysql import OperationMysql
from datetime import datetime


def getUserPoetryDetails():
    oper = OperationMysql()
    userlist = oper.search_all("select id,name from User;")
    detailslist = []
    for user in userlist:
        details = dict()
        details["name"] = user["name"]
        details["id"] = user["id"]
        userTagPoetryCount = oper.search_one(
            "select count(tag_end) as count from poetry where tag_by = \'{}\'".format(user["name"]))
        details["count"] = userTagPoetryCount["count"]
        details["display_time"] = datetime.now()
        detailslist.append(details)
    return detailslist


if __name__ == '__main__':
    getUserPoetryDetails()
