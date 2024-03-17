#!/usr/bin/env python3
# encoding=utf-8

# NOTE: this template script uses Python 3 syntax, edit the hashbang above
#       or use __future__ imports if you'll be running this using Python 2

# script downloaded from Hansken Expert UI (version 532, 2023-10-16T12:32:18.326Z)
# with Hansken (build 47.6.0-academic, 2023-11-09T17:33:57.266Z)
# see https://training.hansken.org/docs/python/ for additional information

# this template script will read connection and authentication details from
# both the command line and environment variables, see
#   python3 [this_script.py] --help
# and the documentation to learn more

from hansken.tool import run

from hanskencase.export import to_folder

# we define a function to do the things we want to do
def search_and_process(context):
    # our argument "context" is a hansken.remote.ProjectContext, see the docs
    # for what it can do other than searching for traces
    with context:
        # query was copied from Hansken Expert UI
        query = ''' tags:mobidoc '''
        # search for traces matching the query
        results = context.search(query)

        print(type(results))

        to_folder(list(results))

        for trace in results:
            # process the results, print some details for each trace we've found
            print(trace.uid, trace.name)


if __name__ == '__main__':
    # call the hansken.py command line, but make it call our function
    run(with_context=search_and_process,
        # the gatekeeper REST endpoint when this script was exported, note that
        # this can be overridden by passing -e/--endpoint on the command line
        endpoint='https://training.hansken.org/gatekeeper/',
        # the keystore REST endpoint when this script was exported, note that
        # this can be overridden with --keystore
        keystore='https://training.hansken.org/keystore/',
        # the project id of the project named "Hansken Demo",
        project='46e3854e-9166-4f8c-b898-b79ac968e0c6')
