from setuptools import find_packages, setup

setup(
    packages=find_packages(exclude=('example', 'tests', 'docs'))
)
