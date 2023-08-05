from os import path

from setuptools import setup


def readme():
    this_directory = path.abspath(path.dirname(__file__))
    with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
        return f.read()


setup(
    name="json-analyze",
    version="0.3.0",
    description="A small tool to check JSON data for structural and data inconsistencies.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/json-analyze/",
    author="Tobias Ammann",
    author_email="tammann@ergonomics.ch",
    license="MIT",
    py_modules=["json_analyze"],
    install_requires=["jsonpath-ng", "tabulate"],
    entry_points={
        "console_scripts": ["json-analyze=json_analyze:main"],
    },
    zip_safe=False,
)
