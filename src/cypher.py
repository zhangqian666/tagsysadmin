# -*- coding: utf-8 -*-
from common.graph import get_graph
from common.constant import entity_Ner, entity_attribute, entity_main_attribute

"""
功能 ： 用于 获取实体相关信息

developer ： 雷艳

"""


class Cypher():

    @staticmethod
    def get_entity(context, ner):
        sql = "Match (n: {entity_ner}) where n.{entity_attr} = '{entity_context}' return n".format(
            entity_ner=ner,
            entity_attr=entity_attribute[ner],
            entity_context=context
        )
        result_list = get_graph().run(sql).data()
        entities = []
        for index in range(len(result_list)):
            entity = {}
            entity['ID'] = result_list[index]['n'].identity
            for attr in entity_main_attribute[ner]:
                entity[attr] = dict(result_list[index]['n']).get(attr, '')
            entities.append(entity)
        return entities


if __name__ == '__main__':
    Cypher.get_entity("玉楼春", "Poetry")
    str = "MATCH (n:Dynasty) RETURN n LIMIT 25"
    print(get_graph().run(str).data())
