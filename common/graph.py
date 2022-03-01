# -*- coding: utf-8 -*-


from py2neo import Graph
from flask import current_app


def get_graph():
    graph = Graph(
        current_app.config.get("NEO4J_URL"), auth=("neo4j","123456"))
    return graph
