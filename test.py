# -*- coding: utf-8 -*-

"""
@author: zhangqian

@contact: 

@Created on: 2021-04-18 10:55
"""

from add_templete_model import qa
import json

num = 0
with open("src/question_answer_data_add_answerid.txt", encoding="utf-8", mode="r") as f:
    for i in f.readlines():
        line = json.loads(i)
        num = num + 1
        print("num : {} {} {}".format(num, line["question"], line["answer"]))
        if line["answerid"] == "literal":
            continue
        qa.add_template_by_ner(line["question"], line["answer"], line["answerid"])
