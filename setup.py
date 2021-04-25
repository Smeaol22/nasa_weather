# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='nasa_weather',
    version='0.1.0',
    description='historical weather data',
    long_description=readme,
    author='Dauloudet Olivier',
    url='https://github.com/Smeaol22/nasa_weather.git',
    license=license,
    packages=find_packages(exclude='tests')
)
