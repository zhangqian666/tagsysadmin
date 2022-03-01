# -*- coding: utf-8 -*-

"""
@author: zhangqian

@contact: 

@Created on: 2021-04-18 10:55
"""

from add_templete_model import qa
import json

with open("./question_answer_data.txt", encoding="utf-8", mode="r") as f:
    for i in f.readlines():
        line = json.loads(i)
        print("{} {}".format(line["question"], line["answer"]))
        qa.add_template_by_ner(line["question"], line["question"])
