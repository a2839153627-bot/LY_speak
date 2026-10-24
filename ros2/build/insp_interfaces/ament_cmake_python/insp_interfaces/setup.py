from setuptools import find_packages
from setuptools import setup

setup(
    name='insp_interfaces',
    version='0.1.0',
    packages=find_packages(
        include=('insp_interfaces', 'insp_interfaces.*')),
)
