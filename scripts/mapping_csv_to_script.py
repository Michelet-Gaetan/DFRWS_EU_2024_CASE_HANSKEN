import csv

reserved_words = ["False", "def", "if", "raise", "None", "del", "import", "return", "True", "elif", "in", "try", "and",
                  "else", "is", "while", "as", "except", "lambda", "with", "assert", "finally", "nonlocal", "yield",
                  "break", "for", "not", "class", "from", "or", "continue", "global", "pass"]


def derive_common_name(entity_name, position=0):
    entity_common = ""
    first_letter = True
    splitted = entity_name.split(':')[position]
    for i in splitted:
        if i.islower() or first_letter or i == "_":
            entity_common += i
        else:
            entity_common += "_" + i
        first_letter = False
    entity_common = entity_common.lower()
    if entity_common in reserved_words:
        entity_common = "_" + entity_common
    return entity_common


def add_dependencies(script):
    script += "from uuid import uuid4\n\n"
#    script += ("from rdflib import Graph\nfrom hansken.recipes.export import data_stream\nfrom hansken.util import "
#               "parse_datetime\n\n")
#    script += ("from .email_address import add_email_address, get_email_address\n"
#               "from .utils import add_misc_map, get_misc_map\n")
    script += "import io\n\n"
    script += "from hanskencase.namespaces import UCO_OBSERVABLE, Literal, KB, RDF, UCO_CORE\n\n"
    script += "import re\n\n"
    script += "rgx = re.compile('\"(.*)\".*<(.*)>')\n"
    return script


def write_function(entity, rows, script):
    entity_common = derive_common_name(entity, 1)
    if entity=="observable:EmailAccount" or entity=="observable:EmailAccountFacet" or entity=="observable:EmailAddress" or entity=="observable:EmailAddressFacet":
        script += "def add_" + entity_common + "(graph, address):\n"
    else:
        script += "def add_" + entity_common + "(graph, trace):\n"
    script += "\t" + entity_common + " = KB[f\"" + entity.split(':')[1] + "-{uuid4()}\"]\n"
    script += "\tgraph.add((" + entity_common + ", RDF.type, UCO_OBSERVABLE." + entity.split(':')[1] + "))\n\n"

    for row in rows:
        if row["property_CASE"] == "core:hasFacet":
            target_entity = row["format_CASE"]
            target_entity_common = derive_common_name(target_entity, 2)
            if target_entity.split(":")[2]=="EmailAccountFacet" or target_entity.split(":")[2]=="EmailAddressFacet":
                script += "\t" + target_entity_common + " = add_" + target_entity_common + "(graph,address)\n"
            else:
                script += "\t" + target_entity_common + " = add_" + target_entity_common + "(graph,trace)\n"
            script += "\tgraph.add((" + entity_common + ", UCO_CORE.hasFacet, " + target_entity_common + "))\n\n"

        elif row["format_CASE"] == row["format_hansken"]:
            property_hansken = row["property_hansken"]
            property_hansken_common = derive_common_name(property_hansken)
            entity_hansken = row["entity_hansken"]
            property_case = row["property_CASE"]
            entity_case = row["entity_CASE"]
            type_hansken = row["format_hansken"]
            if row["cardinality_CASE"] == "0 1" and row["cardinality_hansken"] == "0 1":

                if property_case=="observable:body" and entity_case=="observable:EmailMessageFacet":
                    script += '\tbody = ""\n'
                    script += '\tif "plain" in trace.data_types:\n'
                    script += '\t\twith io.TextIOWrapper(trace.open(stream="plain"), encoding="utf-8") as content:\n'
                    script += '\t\t\tbody += content.read()\n'
                    script += "\tgraph.add((" + entity_common + ", UCO_OBSERVABLE." + property_case.split(':')[
                        1] + ", Literal(body)))\n\n"
                    # body = ""
                    # if "plain" in trace.data_types:
                    #     with io.TextIOWrapper(trace.open(stream='plain'), encoding="utf-8") as content:
                    #         body += content.read()
                    # graph.add((email_message_facet, UCO_OBSERVABLE.body, Literal(body)))

                elif property_case == "observable:addressValue" and entity_case=="observable:EmailAddressFacet":
                    script += "\tm = rgx.match(address)\n"
                    script += "\tif m is not None:\n"
                    script += "\t\taddress = m[1]\n"
                    script += "\tgraph.add((" + entity_common + ", UCO_OBSERVABLE." + property_case.split(':')[
                        1] + ", Literal(address)))\n\n"
                elif property_case == "observable:displayName" and entity_case=="observable:EmailAddressFacet":
                    script += "\tm = rgx.match(address)\n"
                    script += "\tif m is not None:\n"
                    script += "\t\tname = m[2]\n"
                    script += "\t\tif name is not None:\n"
                    script += "\t\t\tgraph.add((" + entity_common + ", UCO_OBSERVABLE." + property_case.split(':')[
                        1] + ", Literal(name)))\n\n"
                else:
                    if property_hansken in reserved_words:
                        script += "\t" + property_hansken_common + " = trace." + entity_hansken + '["' + property_hansken + '"]\n'
                    else:
                        script += "\t" + property_hansken_common + " = trace." + entity_hansken + "." + property_hansken + "\n"

                    if type_hansken=="boolean":
                        script += "\tif " + property_hansken_common + " is not None:\n"
                    else:
                        script += "\tif " + property_hansken_common + ":\n"

                    if property_case.split(':')[1] in reserved_words:
                        script += "\t\tgraph.add((" + entity_common + ', UCO_OBSERVABLE["' + property_case.split(':')[
                            1] + '"], Literal(' + property_hansken_common + ")))\n\n"
                    else:
                        script += "\t\tgraph.add((" + entity_common + ", UCO_OBSERVABLE." + property_case.split(':')[
                            1] + ", Literal(" + property_hansken_common + ")))\n\n"

            elif row["cardinality_CASE"] == "0 *" and row["cardinality_hansken"] == "0 *":
                # TODO: add a column in the csv for the type of datastructure used in hansken.
                script += "\t" + property_hansken_common + " = trace." + entity_hansken + "." + property_hansken + " or []\n"
                script += "\tfor string in " + property_hansken_common + ":\n"
                script += "\t\tgraph.add((" + entity_common + ", UCO_OBSERVABLE." + property_case.split(':')[
                    1] + ", Literal(string)))\n\n"

            elif row["cardinality_CASE"] == "0 1" and row["cardinality_hansken"] == "0 *":
                # TODO: add a column in the csv for the type of datastructure used in hansken.
                script += "\t" + property_hansken_common + " = trace." + entity_hansken + "." + property_hansken + " or {}\n"
                script += "\tif " + property_hansken_common + ":\n"
                script += "\t\tgraph.add((" + entity_common + ", UCO_OBSERVABLE." + property_case.split(':')[
                    1] + ", Literal(str(" + property_hansken_common + "))))\n\n"

            else:
                print(row["property_CASE"] + "is not yet supported")

        else: # format_CASE != format_hansken
            property_hansken = row["property_hansken"]
            property_hansken_common = derive_common_name(property_hansken)
            entity_hansken = row["entity_hansken"]
            property_case = row["property_CASE"]
            format_CASE = row["format_CASE"]
            if row["cardinality_CASE"] == "0 1" and row["cardinality_hansken"] == "0 1":
                if property_case=="observable:emailAddress":
                    script += "\tif address :\n"
                    script += "\t\temail_account_facet_entity = add_" + derive_common_name(format_CASE,
                                                                                                       2) + "(graph, address)\n"
                    script += "\t\tgraph.add((" + entity_common + ', UCO_OBSERVABLE.' + property_case.split(':')[
                        1] + ", email_account_facet_entity))\n\n"
                else:
                    if property_hansken in reserved_words:
                        script += "\t" + property_hansken_common + " = trace." + entity_hansken + '["' + property_hansken + '"]\n'
                    else:
                        script += "\t" + property_hansken_common + " = trace." + entity_hansken + "." + property_hansken + "\n"
                    script += "\tif " + property_hansken_common + ":\n"
                    script += "\t\t" + property_hansken_common + "_entity = add_" + derive_common_name(format_CASE,
                                                                                                       2) + "(graph," + property_hansken_common + ")\n"
                    if property_case.split(':')[1] in reserved_words:
                        script += "\t\tgraph.add((" + entity_common + ', UCO_OBSERVABLE["' + property_case.split(':')[
                            1] + '"], ' + property_hansken_common + "_entity))\n\n"
                    else:
                        script += "\t\tgraph.add((" + entity_common + ", UCO_OBSERVABLE." + property_case.split(':')[
                            1] + ", " + property_hansken_common + "_entity))\n\n"

            elif row["cardinality_CASE"] == "0 *" and row["cardinality_hansken"] == "0 *":
                if property_hansken in reserved_words:
                    script += "\t" + property_hansken_common + " = trace." + entity_hansken + '["' + property_hansken + '"] or []\n'
                else:
                    script += "\t" + property_hansken_common + " = trace." + entity_hansken + "." + property_hansken + " or []\n"
                script += "\tfor string in " + property_hansken_common + ":\n"
                script += "\t\t" + property_hansken_common + "_entity = add_" + derive_common_name(format_CASE,
                                                                                                   2) + "(graph, string)\n"
                if property_case.split(':')[1] in reserved_words:
                    script += "\t\tgraph.add((" + entity_common + ', UCO_OBSERVABLE["' + property_case.split(':')[
                        1] + '"], ' + property_hansken_common + "_entity))\n\n"
                else:
                    script += "\t\tgraph.add((" + entity_common + ", UCO_OBSERVABLE." + property_case.split(':')[
                        1] + ", " + property_hansken_common + "_entity))\n\n"
            else:
                print(str(row) + "is not yet supported")


            # TODO: need to implement those new properties!
    script += "\treturn " + entity_common + "\n\n"

    return (script)


if __name__ == '__main__':
    maping_file = "hansken_case_email.csv"
    script_to_write = ""
    # read the CSV file, parse it, and put the results
    with open(maping_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        reader_forever = list(reader)

    set_entity: set = set([entity["entity_CASE"] for entity in reader_forever])
    script_to_write += add_dependencies(script_to_write)
    for entity in set_entity:
        sub_set_reader = [row for row in reader_forever if row['entity_CASE'] == entity]
        script_to_write = write_function(entity, sub_set_reader, script_to_write)

    file_to_write = maping_file.split(".")[0].split("_")[2] + ".py"

    with open("../hanskencase/_" + file_to_write, "w") as py_file:
        py_file.write(script_to_write)