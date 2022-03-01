# -*- coding: utf-8 -*-

from common.graph import get_graph
from common.constant import entity_attr, entity_relation, entity_attribute

"""
功能 ： 用于 获取属性/关系列表

developer ： 雷艳

"""


def get_entity_ner_by_ID(id_):
    # 根据ID获取实体label
    sql = 'match (n) where ID(n) = ' + str(id_) + ' return labels(n) as label'
    try:
        Node = get_graph().run(sql).data()
    except IndexError:
        return ""
    ner = ""
    if Node:
        label = Node[0].get('label', [])
        ner = label[0] if label else ""
    return ner


def get_option_relation(id):
    # 提示可能属性或者关系
    ner = get_entity_ner_by_ID(id)
    return entity_attr.get(ner, []) + entity_relation.get(ner, [])


def predict_second_entity(id, relation):
    # 根据实体1和中间关系或属性, 预测实体2或者属性值
    ner = get_entity_ner_by_ID(id)
    answer = []
    if relation in entity_attr.get(ner, []):  # 属性
        sql = 'Match (n) where ID(n) = {id_} return n.{attr_} as attr'.format(
            id_=id, attr_=relation)
        Node = get_graph().run(sql).data()
        tmp = {
            "ID": "literal",
            "content": Node[0].get('attr', "")
        }
        answer.append(tmp)
    elif relation in entity_relation.get(ner, []):  # 关系
        sql = 'Match (m: {ner_})-[r: {relation_}]->(n) where ID(m) = {id_} return n'.format(
            ner_=ner, relation_=relation, id_=id)
        Node = get_graph().run(sql).data()
        print(Node)
        if not Node:
            return ""
        entity2_ner = ""
        for ner in Node[0]['n']._labels:
            entity2_ner = ner
        for index in range(len(Node)):
            tmp = {
                "ID": Node[index]['n'].identity,
                "content": dict(Node[index]['n']).get(entity_attribute[entity2_ner], "")
            }
            answer.append(tmp)
    else:
        return ""
    return answer
