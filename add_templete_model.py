# -*- coding: utf-8 -*-

"""
@author: zhangqian

@contact: 

@Created on: 2022/3/1 下午2:33
"""
import os, requests, json
import subprocess
from common import constant
from src.backbone_query import BackBone

import hanlp
from hanlp.components.mtl.multi_task_learning import MultiTaskLearning
from hanlp.components.mtl.tasks.tok.tag_tok import TaggingTokenization

HanLP: MultiTaskLearning = hanlp.load(hanlp.pretrained.mtl.CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_SMALL_ZH)
tok: TaggingTokenization = HanLP['tok/fine']

ner_url = "http://172.17.0.5:8000/predict"


class HTTPUtils(object):
    def __ner_request(self, question):
        """网络请求"""
        body = {
            "message": question,
            "userid": "123"
        }
        return requests.get(ner_url, params=body).content.decode()

    def __handle_ner_data(self, question, result):
        print(result)
        all_data = []
        item = result["data"]["data"]["ver"][0]
        seq = ""
        seg_list = list(question)
        for i in range(len(item)):
            label = item[i]
            option = label.split("-")[0]
            if option == "B" or option == "O":
                if seq != "":
                    all_data.append({
                        "words": seq,
                        "type": item[i - 1].split("-")[1]
                    })
                    seq = ""
            if option == "B" or option == "I":
                seq += seg_list[i]
        if seq != "":
            all_data.append({
                "words": seq,
                "type": item[-1].split("-")[1]
            })
        return all_data

    def get_ner(self, question):
        try:
            result = json.loads(self.__ner_request(question))
            ner = self.__handle_ner_data(question,
                                         result)
        except Exception as e:
            print(e)
            return []
        return ner

    def get_ner_by_id(self, sentence):
        pass


class WeightedTree():
    def __init__(self):
        self.backbone = BackBone()
        self.content_json = self.load_template()
        self.entity_ner_map = self.constrcut_ner_map()
        self.ner_pos = ["People", "Poetry", "Verse", "Poetrything", "Dynasty", "Location", "Genre"]
        self.esstential_pos = ["NN", "VV"]
        self.http_utils = HTTPUtils()

    def generate_consistency_tree(self, question):
        consistency_tree = HanLP(question)['con']
        return consistency_tree

    def deal_tree_line(self, consistency_tree):
        tree = str(consistency_tree).replace('\n', ' ')
        tree = tree.replace('\t', '')
        tree = ' '.join(tree.split())
        return tree

    def link_entity_ids_by_id(self, answerid):
        entity_ids = []
        optional_entity_list = self.backbone.getentitybyid(answerid)
        if optional_entity_list:
            entity_ids.append({"type": optional_entity_list[0]["labels"]})
        print(entity_ids)
        return entity_ids

    def link_entity_ids_by_line(self, sentence):
        ner = self.http_utils.get_ner(sentence)
        entity_ids = []
        print(ner)
        for item in ner:
            if item["type"] == "Others":
                return []
            if item["type"] == "Verse":
                words = item["words"].split("，")
                for word in words:
                    word = word.replace("”", "")
                    word = word.replace("。", "")
                    word = word.replace("“", "")
                    optional_entity_list = self.backbone.get_entity(word, item["type"])
                    if optional_entity_list:
                        entity_ids.append({"ner": word, "type": item["type"], "link": optional_entity_list[0]})
            else:
                word = item["words"]
                word = word.replace("”", "")
                word = word.replace("。", "")
                word = word.replace("“", "")
                optional_entity_list = self.backbone.get_entity(word, item["type"])
                if optional_entity_list:
                    entity_ids.append({"ner": word, "type": item["type"], "link": optional_entity_list[0]})
        print(entity_ids)
        return entity_ids

    def constrcut_ner_map(self):
        fileNames = os.listdir(constant.dict_path)
        entity_ner_map = {}
        for filename in fileNames:
            entity_ner_map[filename.strip('.txt')] = set(constant.read_data(constant.dict_path + filename, flag=True))
        dic = set()
        for key in entity_ner_map.keys():
            dic = dic | entity_ner_map[key]
        tok.dict_force = dic
        return entity_ner_map

    def judge_chinese(self, ch):
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
        elif ch in [u'\u3002', u'\uff1b', u'\uff0c', u'\uff1a', u'\u201d', u'\uff08', u'\uff09', u'\u3001', u'\uff1f',
                    u'\u300a', u'\u300b']:
            return True
        else:
            return False

    def find_first_chinese_char(self, consistency_tree, index):
        while (index < len(consistency_tree)):
            if self.judge_chinese(consistency_tree[index]):
                break
            else:
                index += 1
        return index

    def get_pos_from_chinese_str(self, chinese_str):
        # make 网络请求

        for key in self.ner_pos:
            if chinese_str in self.entity_ner_map[key]:
                return key
        return ""

    def get_pos_from_weighted_tree(self, weighted_tree):
        index = len(weighted_tree) - 2
        pos = ''
        while (index > 0):
            if weighted_tree[index] != '(':
                pos = weighted_tree[index] + pos
            else:
                # print(weighted_tree, pos)
                return pos
            index -= 1

    def get_pos_from_chinese_str(self, chinese_str):
        for key in self.ner_pos:
            if chinese_str in self.entity_ner_map[key]:
                return key
        return ""

    def get_weight_from_chinese_str(self, pos):
        weight = 0
        if pos in self.esstential_pos:
            weight = 0.3
        elif pos in self.ner_pos:
            weight = 0.4
        else:
            weight = 0.1
        # print(pos, weight)
        return weight

    def generalize_entity(self, consistency_tree, weighted_tree, last_chinese_end_index, chinese_begin_index):
        weighted_tree = weighted_tree + consistency_tree[last_chinese_end_index:chinese_begin_index]
        loc = chinese_begin_index
        while (loc < len(consistency_tree)):
            if self.judge_chinese(consistency_tree[loc]):
                loc += 1
            else:
                break
        chinese_begin = chinese_begin_index
        weight_begin = loc
        chinese_str = consistency_tree[chinese_begin: weight_begin]
        standard_pos = self.get_pos_from_weighted_tree(weighted_tree)
        ner_pos = self.get_pos_from_chinese_str(chinese_str)
        if ner_pos:
            standard_pos = ner_pos
            weighted_tree += ner_pos  # 对实体进行泛化
        else:
            weighted_tree += chinese_str
        weight = self.get_weight_from_chinese_str(standard_pos)
        weighted_tree += ":"
        weighted_tree += str(weight)
        return loc, weighted_tree

    def add_weight_to_tree(self, consistency_tree):
        weighted_tree = ''
        index = 0
        while (index < len(consistency_tree)):
            first_chinese_index = self.find_first_chinese_char(consistency_tree, index)  # 找到从index开始遇到的第一个中文符号
            if first_chinese_index >= len(consistency_tree):  # 后面没有中文字符，直接复制
                break
            chinese_end_next, weighted_tree = self.generalize_entity(consistency_tree, weighted_tree, index,
                                                                     first_chinese_index)  # 遇到中文符号就处理，实体泛化，加入权重
            index = chinese_end_next  # 记录中文串结束后的位置
        weighted_tree += consistency_tree[index:len(consistency_tree)]
        return weighted_tree

    def get_weighted_tree(self, query):
        consistency_tree = self.generate_consistency_tree(query)
        consistency_tree = self.deal_tree_line(consistency_tree)
        weighted_tree = self.add_weight_to_tree(consistency_tree)
        return weighted_tree

    def input_entitiy_link_data(self, context):
        input_contexts = []
        tmp = input(context)
        while (tmp != '0'):
            input_contexts.append(tmp)
            tmp = input(context)
        return input_contexts

    def add_id_to_json(self, question):
        entity_ids = self.input_entitiy_link_data("实体id: ")
        ans_ids = self.input_entitiy_link_data("答案id: ")
        ans_attrs = self.input_entitiy_link_data("答案attribute: ")
        return entity_ids, ans_ids, ans_attrs

    def generate_cypher(self, entity_ids, ans_ids):
        cypher = self.backbone.search_shortest_path(entity_ids, ans_ids)
        return cypher

    def save_template(self):
        constant.save_data(constant.json_path, {"data": self.content_json}, flag=True, isjson=True)

    def add_question_to_db(self, question_data):
        cypher = self.generate_cypher(question_data['entity_ids'], question_data['ans_ids'])
        if cypher is None:
            return
        tree = self.get_weighted_tree(question_data['question'])
        question_data['cypher'] = cypher
        question_data['tree'] = tree
        constant.append_data(constant.add_weight_trees_path, tree, flag=True)
        self.content_json.append(question_data)
        self.save_template()
        print("save end : {}".format(question_data))
        return question_data

    def load_template(self):
        self.content_json = constant.read_data(constant.json_path, isjson=True)['data']
        return self.content_json

    def add_template_by_ner(self, question, answer, answerid):
        entity_ids = [str(item['link']['ID']) for item in self.link_entity_ids_by_line(question)]
        ans_ids = [answerid]
        ans_attrs = [item['type'].lower() + "Name" for item in self.link_entity_ids_by_id(answerid)]
        question_data = {"question": question, "entity_ids": entity_ids, "answer": answer, "ans_ids": ans_ids,
                         "ans_attr:": ans_attrs}
        if len(entity_ids) == 0 or len(ans_ids) == 0 or len(ans_attrs) == 0:
            return
        return self.add_question_to_db(question_data)


qa = WeightedTree()
