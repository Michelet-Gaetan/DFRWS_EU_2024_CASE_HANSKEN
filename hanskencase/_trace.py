from uuid import uuid4

from .namespaces import HANSKEN, KB, Literal, RDF, UCO_CORE, UCO_OBSERVABLE
from ._image import add_image


def add_trace(graph, trace):
    _id = trace.get("uid") or trace.get("id") or uuid4()
    trace_kb = KB[f"Trace-{_id}"]

    graph.add((trace_kb, RDF.type, HANSKEN.Trace))

    dscr = trace.get("description")
    if dscr:
        graph.add((trace_kb, UCO_CORE.description, Literal(dscr)))

    image = add_image(graph, trace)
    graph.add((trace_kb, HANSKEN.image, image))

    mv = trace.get("model_version")
    if mv:
        graph.add((trace_kb, HANSKEN.modelVersion, Literal(mv)))

    name = trace.get("name")
    if name:
        graph.add((trace_kb, UCO_CORE.name, Literal(name)))

    # parent -- maybe use with UCO_OBSERVABLE.ObservableRelationship
    # or maybe with the observable:PathRelationFacet
    return trace_kb
