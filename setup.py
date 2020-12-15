# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

PROJECT_URL = ''

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name = 'geopbf',
    version = '0.1.0',
    description = 'Helper package for developing vector tiles service',
    long_description = readme,
    author = 'Manuele Pesenti',
    author_email = 'manuele@inventati.org',
    url = PROJECT_URL,
    license = license,
    packages = find_packages(exclude=('tests', 'docs')),
    install_requires=[
        # Requirements goes here
        # Eg.: "caldav == 0.1.4",
        "shapely",
        "mercantile",
        "pyproj",
        # "py4web",
        "mapbox_vector_tile"
    ]
)
