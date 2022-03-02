# -*- coding: utf-8 -*-

'''
Descripttion: 
Author: Leiyan
Date: 2021-05-10 09:40:17
LastEditTime: 2021-05-28 23:18:21
'''
from py2neo import Graph, Node
from common.constant import entity_attribute, entity_main_attribute
import pymysql  # 导入 pymysql
import re


# "http://localhost/",
# "http://39.105.121.160:27474/",
#  "http://192.168.1.106:7474/",
class BackBone():
    def __init__(self):
        self.graph = self.get_graph()
        self.entity_id_to_name_map = {}
        self.ans_id_to_namae_map = {}

    def get_graph(self):
        graph = Graph("http://172.17.0.4:7474/", auth=("neo4j", "123456"))
        return graph

    def update_verseBelongTo_reverse(self):
        sql = 'MATCH (a:Verse)<-[r:verseBelongTo]-(b:Poetry) MERGE (a)-[r1:verseBelongTo]->(b)'
        self.graph.run(sql)
        # sql = 'MATCH (a:Verse)<-[r:verseBelongTo]-(b:Poetry) delete r'
        # self.graph.run(sql)

    def update_verseBelongTo_people(self):
        sql = 'MATCH (a:Verse)-[r:verseBelongTo]->(b:People), (c:Poetry) where a.poetryId = c.poetryId MERGE (a)-[r1:verseBelongTo]->(c)'
        self.graph.run(sql)
        sql = 'MATCH (a:Verse)-[r:verseBelongTo]->(b:People) delete r'
        self.graph.run(sql)

    def generalize_path(self, path):
        path = path.replace('_', '')
        for key, value in self.ans_id_to_namae_map.items():
            path = path.replace(key, 'ans')
            print(path)
        for key, value in self.entity_id_to_name_map.items():
            path = path.replace(key, 'ent_' + str(value))
            print(path)
        valiables = re.findall('\(([^_][0-9]+)\)', path)
        for value in valiables:
            path = path.replace(value, '')
            print(path)
        print(path)
        return path

    def excute_cypher(self, cypher):
        data = self.graph.run(cypher).data()
        return data

    def getentitybyid(self, id):
        sql = "MATCH (n) WHERE ID(n) = {} RETURN labels(n)".format(id)
        result_list = self.excute_cypher(sql)
        print(result_list)
        entities = []
        for index in range(len(result_list)):
            entity = {}
            entity['labels'] = result_list[index]["labels(n)"][0]
            entities.append(entity)
        print(entities)
        return entities

    def get_entity(self, context, ner):
        sql = "Match (n: {entity_ner}) where n.{entity_attr} = '{entity_context}' return n".format(
            entity_ner=ner,
            entity_attr=entity_attribute[ner],
            entity_context=context
        )
        result_list = self.excute_cypher(sql)
        entities = []
        for index in range(len(result_list)):
            entity = {}
            entity['ID'] = result_list[index]['n'].identity
            for attr in entity_main_attribute[ner]:
                entity[attr] = dict(result_list[index]['n']).get(attr, '')
            entities.append(entity)
        return entities

    def search_shortest_path(self, entity_ids, ans_id):
        self.entity_id_to_name_map = {}
        self.ans_id_to_namae_map = {}
        for index in range(len(entity_ids)):
            self.entity_id_to_name_map[entity_ids[index]] = index
        for index in range(len(ans_id)):
            self.ans_id_to_namae_map[ans_id[index]] = index
        node_ids = list(set(entity_ids + ans_id))
        sql = "match (n) where ID(n) in [{}] with collect(n) as nds unwind nds as n1 unwind nds as n2 with nds,n1,n2 where id(n1)>id(n2) match path=ShortestPath((n1)-[r*..3]-(n2)) with nds, path where all(n in nds where n in nodes(path)) return path order by length(path) asc".format(
            ",".join(node_ids))
        # sql = "MATCH (n) WHERE id(n) in [{}] CALL apoc.path.subgraphAll(n, {{maxLevel:2,bfs:true,endNodes:n,limit:1}}) YIELD nodes,relationships RETURN nodes,relationships".format(",".join(node_ids))
        print(sql)
        data = self.graph.run(sql).data()
        print(data)
        id_to_role_map = {}
        for index in range(len(node_ids)):
            id_to_role_map[node_ids[index]] = "ent_{}".format(index)
        id_to_role_map[node_ids[len(node_ids) - 1]] = "ans"
        for path in data:
            print(str(path['path']))
            return self.generalize_path(str(path['path']))

# query_template = BackBone()
# entity_ids = ['264841','269661','43177','43178']
# ans_id = ['289071']
# query_template.search_shortest_path(entity_ids, ans_id)
# query_template.update_verseBelongTo_people()
# query_template.update_verseBelongTo_reverse()
