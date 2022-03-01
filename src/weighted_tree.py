# -*- coding: utf-8 -*-

'''
Descripttion: 
Author: Leiyan
Date: 2021-04-29 16:09:05
LastEditTime: 2021-05-29 09:33:31
'''
import os
import subprocess
import hanlp
from hanlp.components.mtl.multi_task_learning import MultiTaskLearning
from hanlp.components.mtl.tasks.tok.tag_tok import TaggingTokenization
from common import constant
from src.backbone_query import BackBone

HanLP: MultiTaskLearning = hanlp.load(hanlp.pretrained.mtl.CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_SMALL_ZH)
tok: TaggingTokenization = HanLP['tok/fine']
from src.cypher import Cypher


class WeightedTree():
    def __init__(self):
        self.entity_ner_map = self.constrcut_ner_map()
        self.ner_pos = ["People", "Poetry", "Verse", "Poetrything", "Dynasty", "Location", "Genre"]
        self.esstential_pos = ["NN", "VV"]
        self.backbone = BackBone()
        self.content_json = self.load_template()

    def generate_consistency_tree(self, question):
        consistency_tree = HanLP(question)['con']
        return consistency_tree

    def generate_dependency_parse_tree(self, question):
        conll = HanLP(question)['dep']
        constant.save_data(constant.conll_path, str(conll))

    def deal_tree_line(self, consistency_tree):
        tree = str(consistency_tree).replace('\n', ' ')
        tree = tree.replace('\t', '')
        tree = ' '.join(tree.split())
        return tree

    def link_entity_ids(self, sentence):
        tokens = HanLP(sentence)['tok/fine']
        print(tokens)
        entity_ids = []
        for words in tokens:
            ner = self.get_pos_from_chinese_str(words)
            print(words, ner)
            if ner:
                optional_entity_list = Cypher.get_entity(words, ner)
                print(optional_entity_list)
                if optional_entity_list:
                    entity_ids.append({"ner": words, "type": ner, "link": optional_entity_list[0]})
        print(entity_ids)
        return entity_ids

    def link_entity_ids_by_line(self, sentence):
        ner = online_ner(sentence)
        entity_ids = []
        print(ner)
        for item in ner:
            optional_entity_list = Cypher.get_entity(item["words"], item["type"])
            if optional_entity_list:
                entity_ids.append({"ner": item["words"], "type": item["type"], "link": optional_entity_list[0]["ID"]})
        print(entity_ids)
        return entity_ids


    def link_entity_ids_by_ner(self, ner):
        entity_ids = []
        print(ner)
        for item in ner:
            optional_entity_list = Cypher.get_entity(item["words"], item["type"])
            if optional_entity_list:
                entity_ids.append({"ner": item["words"], "type": item["type"], "link": optional_entity_list[0]["ID"]})
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
                break;
            chinese_end_next, weighted_tree = self.generalize_entity(consistency_tree, weighted_tree, index,
                                                                     first_chinese_index)  # 遇到中文符号就处理，实体泛化，加入权重
            index = chinese_end_next  # 记录中文串结束后的位置
        weighted_tree += consistency_tree[index:len(consistency_tree)]
        return weighted_tree

    def standard_input_file(self, weighted_tree, existed_trees):
        pairs = []
        for tree in existed_trees:
            one_pair = "|BT| " + weighted_tree + " |BT| " + tree + " |ET|"
            pairs.append(one_pair)
        constant.save_data(constant.final_input_path, pairs, flag=True)

    def save_weighted_tree(self):
        questions = constant.read_data(constant.question_path, flag=True)
        weighted_trees = []
        for question in questions:
            weighted_tree = self.get_weighted_tree(question)
            weighted_trees.append(weighted_tree)
            entity_ids, ans_ids, ans_attrs = self.add_id_to_json(question)
            self.content_json.append(
                {"question": question, "tree": weighted_tree, "entity_ids": entity_ids, "ans_ids": ans_ids,
                 "ans_attrs": ans_attrs})
        constant.save_data(constant.add_weight_trees_path, weighted_trees, flag=True)

    def read_weighted_tree(self):
        existed_trees = constant.read_data(constant.add_weight_trees_path, flag=True)
        return existed_trees

    def get_weighted_tree(self, query):
        consistency_tree = self.generate_consistency_tree(query)
        consistency_tree = self.deal_tree_line(consistency_tree)
        weighted_tree = self.add_weight_to_tree(consistency_tree)
        return weighted_tree

    def constrcut_two_pairs(self, query):
        weighted_tree = self.get_weighted_tree(query)
        existed_trees = self.read_weighted_tree()
        self.standard_input_file(weighted_tree, existed_trees)

    def input_entitiy_link_data(self, context):
        input_contexts = []
        tmp = input(context)
        while (tmp != '0'):
            input_contexts.append(tmp)
            tmp = input(context)
        return input_contexts

    def add_id_to_json(self, question):
        print(question)
        entity_ids = self.input_entitiy_link_data("实体id: ")
        ans_ids = self.input_entitiy_link_data("答案id: ")
        ans_attrs = self.input_entitiy_link_data("答案attribute: ")
        return entity_ids, ans_ids, ans_attrs

    def generate_cypher(self, entity_ids, ans_ids):
        cypher = self.backbone.search_shortest_path(entity_ids, ans_ids)
        return cypher

    def save_template(self):
        constant.save_data(constant.json_path, {"data": self.content_json}, flag=True, isjson=True)

    def add_cypher_to_json(self):
        self.save_weighted_tree()
        # self.constrcut_two_pairs(question)
        for data in self.content_json:
            cypher = self.generate_cypher(data['entity_ids'], data['ans_ids'])
            data['cypher'] = cypher
            print("cypher:", cypher)
        self.save_template()

    def add_question_to_db(self, question_data):
        print(question_data)
        cypher = self.generate_cypher(question_data['entity_ids'], question_data['ans_ids'])
        tree = self.get_weighted_tree(question_data['question'])
        question_data['cypher'] = cypher
        question_data['tree'] = tree
        constant.append_data(constant.add_weight_trees_path, tree, flag=True)
        self.content_json.append(question_data)
        self.save_template()
        print(question_data)
        return question_data

    def add_template(self, question, answer):
        entity_ids = [str(item['link']['ID']) for item in self.link_entity_ids(question)]
        ans_ids = [str(item['link']['ID']) for item in self.link_entity_ids(answer)]
        ans_attrs = [item['type'].lower() + "Name" for item in self.link_entity_ids(answer)]
        question_data = {"question": question, "entity_ids": entity_ids, "answer": answer, "ans_ids": ans_ids,
                         "ans_attr:": ans_attrs}
        return self.add_question_to_db(question_data)

    def load_template(self):
        self.content_json = constant.read_data(constant.json_path, isjson=True)['data']
        return self.content_json

    def rank_template(self):
        print("----exec")
        ret = subprocess.run(["/Users/zhangqian/tagsysadmin/src/rank.sh"])
        print("ret: ", ret)
        rank_template = constant.read_data(constant.score_path, flag=True)
        index = rank_template.index(max(rank_template))
        print("index:", index)
        return index

    def add_template_by_ner(self, question, answer):
        entity_ids = [str(item['link']['ID']) for item in self.link_entity_ids(question)]
        ans_ids = [str(item['link']['ID']) for item in self.link_entity_ids(answer)]
        ans_attrs = [item['type'].lower() + "Name" for item in self.link_entity_ids(answer)]
        question_data = {"question": question, "entity_ids": entity_ids, "answer": answer, "ans_ids": ans_ids,
                         "ans_attr:": ans_attrs}
        return self.add_question_to_db(question_data)

    def acvt_handle(self, question, ner):
        entity_ids = self.link_entity_ids_by_ner(ner)
        one_question = {"question": question, "entity_ids": entity_ids}
        print("{},{}".format(question, entity_ids))
        self.constrcut_two_pairs(one_question['question'])
        index = self.rank_template()
        print(index, self.content_json[index])
        cypher = self.content_json[index]['cypher']
        entity_id_strs = ""
        for idd in range(len(entity_ids)):
            if "ent_{}".format(idd) in cypher:
                entity_id_strs += "id(ent_{index}) = {id} and ".format(index=idd, id=entity_ids[idd]["link"])
        entity_id_strs = entity_id_strs[:len(entity_id_strs) - 5]

        sql = "match {cypher}  where {entity_id_strs} return distinct labels(ans) as label, ans limit 5".format(
            cypher=cypher, entity_id_strs=entity_id_strs)

        print(sql)
        print(cypher, "---", entity_id_strs)

        execute_data = self.backbone.excute_cypher(sql)
        print("execute_data:", execute_data)
        ner = execute_data[0]['label'][0]
        result = []
        for data in execute_data:
            tmp = {}
            data = dict(data['ans'])
            for attr in constant.entity_main_attribute[ner]:
                tmp[attr] = data.get(attr, "")
            result.append(tmp)
        answer_data = [{"question": self.content_json[index]['question'], "cypher": cypher, "answer": result}]
        print("ans: ", answer_data)
        return answer_data

    def online_qa(self, question):
        entity_ids = [str(item['link']['ID']) for item in self.link_entity_ids(question)]
        one_question = {"question": question, "entity_ids": entity_ids}
        self.constrcut_two_pairs(one_question['question'])
        index = self.rank_template()
        print(index, self.content_json[index])
        cypher = self.content_json[index]['cypher']
        entity_id_strs = ""
        for idd in range(len(entity_ids)):
            if "ent_{}".format(idd) in cypher:
                entity_id_strs += "id(ent_{index}) = {id} and ".format(index=idd, id=entity_ids[idd])
        entity_id_strs = entity_id_strs[:len(entity_id_strs) - 5]

        sql = "match {cypher}  where {entity_id_strs} return distinct labels(ans) as label, ans limit 5".format(
            cypher=cypher, entity_id_strs=entity_id_strs)

        print(sql)
        print(cypher, "---", entity_id_strs)

        execute_data = self.backbone.excute_cypher(sql)
        print("execute_data:", execute_data)
        ner = execute_data[0]['label'][0]
        result = []
        for data in execute_data:
            tmp = {}
            data = dict(data['ans'])
            for attr in constant.entity_main_attribute[ner]:
                tmp[attr] = data.get(attr, "")
            result.append(tmp)
        answer_data = [{"question": self.content_json[index]['question'], "cypher": cypher, "answer": result}]
        print("ans: ", answer_data)
        return answer_data


qa = WeightedTree()
# tree = WeightedTree()
# # question = "“千门万户曈曈日，总把新桃换旧符”中的“旧符”是什么意思？"
# # tree.save_weighted_tree()
# # tree.constrcut_two_pairs(question)
# # tree.generate_dependency_parse_tree(question)
# one_question = "李白是哪个朝代的？"
# # tree.add_cypher_to_json()
# tree.load_template()
# # question_data = {
# #     "question": "“每逢佳节倍思亲”诗句的作者是？",
# #     "entity_ids": ["2601"],
# #     "ans_ids": ["264835"],
# #     "ans_attrs":["peopleName"]
# # }
# # tree.add_question_to_db(question_data)
# one_question = {
#     "question": "“造化钟神秀”的作者是？",
#     "entity_ids": ["7539"]
# }
# tree.online_qa(one_question)
