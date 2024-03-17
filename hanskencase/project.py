import os

from hansken.connect import connect_project

def get_project():
    """Conveniently get project context from environment variables"""
    url = os.getenv("HANSKEN_URL", "https://training.hansken.org/gatekeeper/")
    keystore = os.getenv("HANSKEN_KS", "https://training.hansken.org/keystore/")
    # default project: Hansken Demo project
    project = os.getenv("HANSKEN_PROJECT", "46e3854e-9166-4f8c-b898-b79ac968e0c6")

    # username = os.getenv("HANSKEN_USER")
    # password = os.getenv("HANSKEN_PASS")

    context = connect_project(
        url,
        project,
        keystore=keystore,
        username="hansken115",
        password="7OKIZEZU",
    )

    return context
