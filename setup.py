from setuptools import setup, find_packages
import pathlib


if __name__ == "__main__":
    here = pathlib.Path(__file__).parent.resolve()
    long_description = (here / "README.md").read_text()

    setup(
        name="hanskencase",
        version="0.1",
        description="Hansken CASE integration",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://hansken.org/",
        author="Netherlands Forensic Institute",
        author_email="hansken-support@nfi.nl",
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
        ],
        keywords="CASE,NFI,Hansken",
        packages=find_packages(where="."),
        python_requires=">=3.7, <4",
        install_requires=[
            "hansken",
            "rdflib",
            "requests[socks]",
        ],
    )
