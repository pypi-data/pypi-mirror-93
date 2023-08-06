from setuptools import Extension, setup, find_packages

with open("README.md","r") as fh:
    long_description = fh.read()

sourcefiles = ['ipyconsol.c']
extensions = [Extension("ucla_geotech_tools.ipyconsol",sourcefiles)]

setup(
    name="ucla_geotech_tools-ipyconsol",
    version="1.0.4",
    author="Scott J. Brandenberg",
    author_email="sjbrandenberg@ucla.edu",
    description="Python implementation of iConsol program for computing nonlinear consolidation of soil.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    ext_modules=[Extension('ucla_geotech_tools.ipyconsol',['ipyconsol.c'])],
    namespace_packages=['ucla_geotech_tools']
)