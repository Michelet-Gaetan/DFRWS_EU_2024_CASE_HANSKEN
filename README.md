# Documentation

This repository contains a custom version of the case-hansken Proof of Concept code developed by the NFI. You can find it [here](https://github.com/NetherlandsForensicInstitute/hansken-case/tree/main) This version was created for the DFRWS EU 2024 CASEWorks workshop. Please keep in mind that all python scripts present in this repository are Proofs of Concept and still under development. They might therefore contain bugs and errors. The purpose of this project is to export [Hansken](https://hansken.org/) traces in the [CASE](https://caseontology.org) json-format.

## Original Repository

If you want to learn more about the status of the project, you can go and check the previously mentioned link to the original hansken-case repository. Note that one script was added for this workshop. The purpose of this script is to automatically generate the functions to export a particular Hansken artifact to its "CASE equivalent".

# Workshop

In the _project.py_ file, the environment variables as well as the default are found and/or can be configured. This is where you will have to enter the provided credentials before running other scripts!

The mapping_csv_to_script.py file is there to automatically generate the transformation functions for the emails and chatMessages. This is done using a CSV file describing the maping between the Hansken trace model and the CASE ontology. To generate those functions, simply run the file and adjust the maping_file (line 179) variable to generate the correct function. This should be either "hansken_case_email.csv" or "hansken_case_chat.csv".

You can the run the other scripts (export_example_email.py / export_example_chat.py / export_example_global.py) to transform the extracted emails, extracted chatmessages or both of them into CASE json-ld format.

Finally, visualize the generated CASE graphs using the visualize.py file and rdflib, or using this [rdf online viewer](https://issemantic.net/rdf-visualizer).

## Help

Do not hesitate to ask for help!

## Disclaimer

The material on this repository was made in a research project and is not intended for commercial use with a high TRL.
