# Copyright (c) 2010, Ryan Bourgeois <bluedragonx@gmail.com>
# All rights reserved.
#
# This software is licensed under a modified BSD license as defined in the
# provided license file at the root of this project.  You may modify and/or
# distribute in accordance with those terms.
#
# This software is provided "as is" and any express or implied warranties,
# including, but not limited to, the implied warranties of merchantability and
# fitness for a particular purpose are disclaimed.

from setuptools import setup, find_packages
import sys, os

version = '1.0dev6'

setup(name='whatcouch',
    version=version,
    description="A CouchDB plugin for repoze.what!",
    long_description="""Plugin to extend repoze.who and repoze.what with CouchDB support.  Includes quickstart functionality.""",
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='Python CouchDB CouchDBKit WSGI repoze.who repoze.what authentication authorization',
    author='Ryan Bourgeois',
    author_email='bluedragonx@gmail.com',
    url='http://code.google.com/p/whatcouch/',
    license='BSD-derived (http://code.google.com/p/whatcouch/wiki/License)',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # -*- Extra requirements: -*-
        'couchdbkit >= 0.4.0',
        'repoze.what >=1.0.0, <2.0.0',
        'repoze.who-friendlyform',
        'zope.interface',
        'py_bcrypt'],
    entry_points="""
        # -*- Entry points: -*-
        """)
