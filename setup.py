from setuptools import setup, find_packages, Extension

setup(
    name="precog",
    version="0.1",
    packages=['antlr3'] + find_packages(include=('precog', 'precog.*')),
    author="Glenn Moss",
    author_email="glennimoss@gmail.com",
    url="https://github.com/glennimoss/precog",
    package_dir={'antlr3': 'lib/antlr3'},
    zip_safe=True,
)
