from rdflib import BNode, Graph, Literal, XSD

from .namespaces import RDF, HANSKEN


def add_misc_map(graph: Graph, subject, misc: dict):
    misc = misc or {}
    for key, value in misc.items():
        misc_info = BNode()
        graph.add((misc_info, RDF.type, HANSKEN.MiscInfo))
        graph.add((misc_info, HANSKEN.MiscInfoKey, Literal(key, datatype=XSD.string)))
        graph.add((misc_info, HANSKEN.MiscInfoValue, Literal(value, datatype=XSD.string)))
        # TODO: check -> Does this work?

        graph.add((subject, HANSKEN.hasMiscInfo, misc_info))


def get_misc_map(graph: Graph, subject):
    misc = {}

    misc_items = graph.objects(subject, HANSKEN.hasMiscInfo)
    for misc_item in misc_items:
        keys = list(graph.objects(misc_item, HANSKEN.MiscInfoKey))
        values = list(graph.objects(misc_item, HANSKEN.MiscInfoValue))
        if len(keys) == 1 and len(values) == 1:
            key = str(keys[0])
            value = str(values[0])
            misc[key] = value

    return misc


def add_timestamps(graph: Graph, subject, timestamps: dict):
    timestamps = timestamps or {}

    for _, timestamp in timestamps.items():
        # TODO: incorporate key to reproduce a timestamp dictionary
        graph.add((subject, HANSKEN.hasTimeStamp, Literal(timestamp)))


def get_timestamps(graph: Graph, subject):
    ts = graph.objects(subject, HANSKEN.hasTimeStamp)
    timestamps = {k: str(v) for k, v in enumerate(ts)}

    return timestamps


# def add_created_time(graph, facet, trace_bundle time_type):
#     """ time_type is 'created', 'accessed', 'active', 'expiration', 'modified'"""
#     # createdOn (date) - The date and time of account creation.
#     con = trace_facet.created_on
#     if con:
#         graph.add((account_facet, UCO_OBSERVABLE.createdTime, Literal(con)))


#     # accessedOn (date) - The date and time of the last usage of the account.
#     aon = trace.account.accessed_on
#     if aon:
#         graph.add((account_facet, UCO_OBSERVABLE.accessedTime, Literal(aon)))

#     # active (boolean) - Can the user account be used or is the account disabled or locked.
#     active = trace.account.active
#     if active:
#         graph.add((account_facet, UCO_OBSERVABLE.isActive, Literal(aon)))

#     # expiresOn (date) - The date and time of expiration of the account.
#     eon = trace.account.expires_on
#     if eon:
#         graph.add((account_facet, UCO_OBSERVABLE.expirationTime, Literal(eon)))

#     # misc (map:string) - Additional information about the account.
#     add_misc_map(graph, account_facet, trace.account.misc)
#     # modifiedOn (date) - The date and time of the last modification of the account.
#     mon = trace.account.modified_on
#     if mon:
#         graph.add((account_facet, UCO_OBSERVABLE.modifiedTime, Literal(mon)))
