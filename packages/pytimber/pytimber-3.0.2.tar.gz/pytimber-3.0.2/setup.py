import sys

# XXX This if statement lets you actually build the package
if not 'sdist' in sys.argv:
    sys.exit("""
***

Please install the `pytimber` package

using the https://acc-py-repo.cern.ch package index.

Additional information can be found in:

https://wikis.cern.ch/pages/viewpage.action?pageId=145493385

***\n """)

from setuptools import setup

setup(
    name="pytimber",
    version="3.0.2",
    description="Deprecated package see https://gitlab.cern.ch/scripting-tools/pytimber/"
)
