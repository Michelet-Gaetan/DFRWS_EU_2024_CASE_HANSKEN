# Documentation

This repository contains the Proof of Concept code, developed for exporting Hansken traces in the CASE json-format, and for importing traces presented in [CASE](https://caseontology.org) json-format into [Hansken](https://hansken.org/). Note that this is just a PoC, this code cannot be used for production purposes.

## Status

During this project in which we have looked at integrating HANSKEN and CASE, we have spent approximately six weeks mapping the HANSKEN data model onto the CASE ontology. An important part of this mapping process involved weekly discussions with representatives of the CASE Community and a team of the Netherlands Forensic Institute (NFI). To do this mapping we used existing knowledge within the TNO Data Science Connected Business team.

To record the mapping and discussion we have set up a [google sheet (April 2022)](https://docs.google.com/spreadsheets/d/1zsOYxnQE1KeKCqST1v-n5MD3Zzq7FETGC6ho76E1NG0) describing the HANSKEN CASE mapping. This sheet documents all types of the HANSKEN API. For all types there are gaps between the HANSKEN API and CASE ontology. Often this discrepancy is the _misc_ or _timestamp_ maps, for which we propose to create and use a HANSKEN RDF namespace that extends CASE. For interoperability items from e.g. _misc_ should be moved to named properties that can be mapped explicitly. For extracted property types, most discrepancies can be resolved by extending the CASE ontology. This should be done using change proposals via the CASE Github. Larger gaps between the HANSKEN API and CASE ontology have been identified cryptographic keys and the handling of entities detected by machine learning algorithms. Addressing these gaps is still a considerable amount of work that needs to be taken up in collaboration with the CASE community.

The mapping has been partially implemented as a proof-of-concept for exporting and importing data. This mapping has been done as a best-effort implementation for emails, files and folders, and accounts. The implementation is written in Python using rdflib and the HANSKEN python API. Though the general mapping information is available from the mapping sheet, implementing the mapping typically requires a few more details, This means that implemtation involves looking into the documentation with more details, including into examples. Getting the use of classes and facets right takes some getting used to. During these six weeks a general approach for mapping has been set up and three important types of data mappings have been implemented in the import/export script. As a guideline it is good to expect at least a day of work to implement a mapping for a specific type, once familiar with the CASE ontology and its documentation.

# CASE export and import in Hansken

This repository contains code and documentation on the export and import of Hansken data specified in the [CASE ontology](https://caseontology.org/) metamodel. 

See the [CASE-Hansken Mapping repository](hanskencase) for details on how the Hansken JSON metamodel is mapped to the CASE ontology constructs. 

In the _project.py_ file, the environment variables as well as the default are found and/or can be configured.

## Export/import approach and other options

We built a "manual"/functional import/export script in Python, using [RDFLib](https://rdflib.dev/). We chose this given the limited time of the project, and in order to quickly demo a full round-trip import-export. 

We shortly investigated other approaches. See [the markdown page on Mapping Languages](mapping_languages.md)

## Export model file

The data that is exported from Hansken is stored in a file.
This file contains both the (meta)data (desciption) file in JSON-LD (JavaScript Object Notation - Linked Data) format conform the CASE syntax&semantics, and the actual/raw data files.

The import/export scripts use the Python API of the Hansken Demo environment to get and save the Hansken data.
To be able to export and import data without adding a lot of encoded data to the CASE json-ld file, we propose a simple first version of an export format for Hansken to relate to CASE data. In this format, we provide a CASE compatible metadata export in json-ld and we relate data of objects (e.g., files) as binary files in a local relative filesystem. This boils down to having an export.json-ld file, and an export folder containing the data-files, where the filename corresponds to ... TODO: relate to id or to a special filename triple... For ease of use, we expect this filesystem to be exported and bundled in a zip-file.

Example contents of a zip-file

```sh
./export.json-ld
./export/file1.ext1
./export/file2.ext2
```

Future work involves evaluating the use of for example the [Advanced Forensics File Format (AFF4)](http://www2.aff4.org) standard instead of a simple zip-file. After initial proposals it would be necessary to standards a file format for data and metadata within the CASE community to allow for imports and exports between software supporting CASE.

## Disclaimer

The material on this repository was made in a research project and is not intended for commercial use with a high TRL.
