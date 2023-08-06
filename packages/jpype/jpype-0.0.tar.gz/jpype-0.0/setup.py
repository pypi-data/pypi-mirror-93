import sys

# XXX This if statement lets you actually build the package
if not 'sdist' in sys.argv:
    sys.exit("""
=========================================

Please install the `JPype` with ``pip install jpype1``

=========================================

""")

from distutils.core import setup

setup(
    name="jpype",
    version="0.0",
    description="Unsupported alias for JPype1 (https://pypi.org/project/JPype1/)"
)
