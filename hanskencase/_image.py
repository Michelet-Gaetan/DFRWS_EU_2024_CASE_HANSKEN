from uuid import uuid4

from hansken.util import parse_datetime

from .namespaces import KB, Literal, RDF, UCO_CORE, UCO_OBSERVABLE


def get_image(trace):
    return trace.context.image(trace.image_id)


def add_image_facet(graph, trace):
    image_facet = KB[f"ImageFacet-{uuid4()}"]

    graph.add((image_facet, RDF.type, UCO_OBSERVABLE.ImageFacet))

    image = get_image(trace)

    it = image.get("info", []).get("type")
    if it:
        graph.add((image_facet, UCO_OBSERVABLE.imageType, Literal(it)))

    return image_facet


def add_image(graph, trace):

    image = KB[f"Image-{trace.image_id}"]
    graph.add((image, RDF.type, UCO_OBSERVABLE.Image))

    image_facet = add_image_facet(graph, trace)
    graph.add((image, UCO_CORE.hasFacet, image_facet))

    _image = get_image(trace)

    name = _image.get("name", False)
    if name:
        graph.add((image, UCO_CORE.name, Literal(name)))

    dscr = _image.get("description", False)
    if dscr:
        graph.add((image, UCO_CORE.description, Literal(dscr)))

    cb = _image.get("createdBy", False)
    if cb:
        graph.add((image, UCO_CORE.createdBy, Literal(cb)))

    ct = _image.get("createdDate", False)
    if ct:
        ct = parse_datetime(cb)
        graph.add((image, UCO_CORE.createdTime, Literal(ct)))

    return image
