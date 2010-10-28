from setuptools import setup, find_packages
import sys, os

version = '1.0dev3'

setup(name='whatcouch',
    version=version,
    description="A CouchDB plugin for repoze.what!",
    long_description="""Plugin to extend repoze.who and repoze.what with CouchDB support.  Includes quickstart functionality.""",
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='Python CouchDB CouchDBKit WSGI repoze.who repoze.what authentication authorization',
    author='Ryan Bourgeois',
    author_email='bluedragonx@gmail.com',
    url='http://code.google.com/p/whatcouch/',
    license='GPLv2',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # -*- Extra requirements: -*-
        'couchdbkit >= 0.4.0',
        'repoze.what >=1.0.0, <2.0.0',
        'zope.interface',
        'py_bcrypt'],
    entry_points="""
        # -*- Entry points: -*-
        """)
