# -*- coding: utf-8 -*-

"""
@author: zhangqian

@contact: 

@Created on: 2022/2/13 下午9:49
"""

import pandas as pd
from py2neo import Node, Relationship, Graph, NodeMatcher, RelationshipMatcher


# 创建节点
def CreateNode(m_graph, m_label, m_attrs):
    m_n = "_.name=" + "\'" + m_attrs['name'] + "\'"
    matcher = NodeMatcher(m_graph)
    re_value = matcher.match(m_label).where(m_n).first()
    print(re_value)
    if re_value is None:
        m_mode = Node(m_label, **m_attrs)
        n = graph.create(m_mode)
        return n
    return None


# 查询节点
def MatchNode(m_graph, m_label, m_attrs):
    m_n = "_.name=" + "\'" + m_attrs['name'] + "\'"
    matcher = NodeMatcher(m_graph)
    re_value = matcher.match(m_label).where(m_n).first()
    return re_value


# 创建关系
def CreateRelationship(m_graph, m_label1, m_attrs1, m_label2, m_attrs2, m_r_name):
    reValue1 = MatchNode(m_graph, m_label1, m_attrs1)
    reValue2 = MatchNode(m_graph, m_label2, m_attrs2)
    if reValue1 is None or reValue2 is None:
        return False
    m_r = Relationship(reValue1, m_r_name, reValue2)
    n = graph.create(m_r)
    return n


graph = Graph('http://localhost:27474', username='neo4j', password='123456')

label1 = "Name"
m_r_name = ""


for i in range(1000):
    attr1 = {"name": "tom{}".format(i)}
    CreateNode(graph, label1, attr1)

for i inra
    reValue = CreateRelationship(graph, label1, attr1, label2, attr2, "Father".format("i"))


from py2neo import Graph


class BackBone():
    def __init__(self):
        self.graph = self.get_graph()
        self.entity_id_to_name_map = {}
        self.ans_id_to_namae_map = {}

    def get_graph(self):
        graph = Graph("http://localhost:27474/", auth=("neo4j", "password"))
        return graph

    def excute_cypher(self, cypher):
        data = self.graph.run(cypher).data()
        return data


b = BackBone()

print(b.excute_cypher("match (n) return count(n)"))
print(b.excute_cypher("match ()-->() return count(*)"))