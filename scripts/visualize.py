from rdflib import Graph
import json




graph = Graph()
graph.parse("export/export_test.jsonld", format="json-ld")

#You can then navigate the graph using the functions described in https://rdflib.readthedocs.io/en/stable/intro_to_graphs.html




