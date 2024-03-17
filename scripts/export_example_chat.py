#!/usr/bin/env python3
# encoding=utf-8

# NOTE: this template script uses Python 3 syntax, edit the hashbang above
#       or use __future__ imports if you'll be running this using Python 2

# script downloaded from Hansken Expert UI (version 497, 2022-02-23T09:28:35.454Z)
# with Hansken (build 45.5.0-academic, 2022-03-02T08:38:34.493Z)
# see https://frontend.demo.hansken.org/docs/ for additional information

# this template script will read connection and authentication details from
# both the command line and environment variables, see
#   python3 [this_script.py] --help
# and the documentation to learn more
"""
Export example using the hanskencase wrapper around the Hansken Python API

"""
from hanskencase.project import get_project
from hanskencase.export import to_zip, to_folder

ctx = get_project()
traces = list(ctx.search("tags:WS-chat"))

print(len(traces))
to_folder(traces)
to_zip(traces)
