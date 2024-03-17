import pathlib
import zipfile


from rdflib import Graph
from rdflib.graph import Graph
from hansken.trace import Trace

from . import serialize
from .namespaces import HANSKEN
from ._trace import add_trace

from ._email import add_email_message
from ._chat import add_message


def add_all(graph: Graph, trace: Trace):

    trace_node = add_trace(graph, trace)

    if "email" in trace:
        email_message = add_email_message(graph, trace)
        graph.add((trace_node, HANSKEN.hasData, email_message))

    if "chatMessage" in trace:
        chat_message = add_message(graph, trace)
        graph.add((trace_node, HANSKEN.hasData, chat_message))


def create_graph(traces: list[Trace]):
    if not isinstance(traces, list):
        traces = [traces]

    graph = Graph()

    for trace in traces:
        add_all(graph, trace)

    return graph


def first_data_type(trace, data_types):
    for data_type in data_types:
        if data_type in trace.data_types:
            return data_type
    return False


def get_data_type(trace):
    data_types = ("raw", "html", "html_text", "plain")
    data_type = first_data_type(trace, data_types)
    return data_type


def get_data(trace):
    data_type = get_data_type(trace)
    return trace.open(data_type) if data_type else None


def write_file_to_folder(trace, folder="."):
    path = pathlib.Path(folder)
    with get_data(trace) as buffer:
        with open(path / trace.uid, "wb") as fh:
            fh.write(buffer.read())


def get_filename(trace):
    data_type = get_data_type(trace)
    return f"{trace.uid}.{data_type}"


def to_zip(traces, filename="export.zip"):
    if not isinstance(traces, list):
        traces = [traces]

    g = create_graph(traces)
    with zipfile.ZipFile(filename, "w") as zf:

        with zf.open("export.jsonld", "w") as fh:
            serialize(g, fh)

        for trace in traces:
            if trace.data_types:
                with get_data(trace) as buffer:
                    with zf.open(get_filename(trace), "w") as fh:
                        fh.write(buffer.read())


def to_folder(traces, folder="./export/"):
    if not isinstance(traces, list):
        traces = [traces]
    path = pathlib.Path(folder)
    path.mkdir(exist_ok=True)

    g = create_graph(traces)
    serialize(g, path / "export.jsonld")

    for trace in traces:
        if trace.data_types:
            with get_data(trace) as buffer:
                with open(path / get_filename(trace), "wb") as fh:
                    fh.write(buffer.read())
