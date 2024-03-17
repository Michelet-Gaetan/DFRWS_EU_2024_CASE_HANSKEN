from rdflib.graph import Graph
from .namespaces import context


def serialize(graph: Graph, filename: str):
    graph.serialize(filename, format="json-ld", indent=2, context=context)
