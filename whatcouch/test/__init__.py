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
"""
Nose is used for testing.  You can get it with:
  easy_install nose

And run the tests by cd'ing into the base directory and running:
  nosetests

Package initialization happens here.  The tests are structured around the
Config object defined here.  Setup and teardown methods modify the Config
object defined here.
"""

import sys, couchdbkit
from couchdbkit.loaders import FileSystemDocsLoader

class PackageFixture:
    """
    Handles initial CouchDB setup and teardown.  Also used
    to store configuration for other tests.
    """

    def __init__(self, db_name, design_path):
        """
        Constructor.  Configures the object.
        :param db_name: The name of the database to run tests against.  This database is created on setup and deleted on teardown.
        :param design_path: The path to the design documents to load.
        """
        self.db_name = db_name
        self.design_path = design_path

    def setup(self):
        """
        Creates the test database and loads the design documents.
        """
        self.server = couchdbkit.Server()
        self.db = self.server.create_db(self.db_name)
        loader = FileSystemDocsLoader(self.design_path)
        loader.sync(self.db)

    def teardown(self):
        """
        Deletes the test database.
        """
        self.server.delete_db(self.db_name)

"""Configure the top-level fixture."""
Config = PackageFixture('whatcouch_tests', sys.path[0] + '/_design')

def setup_package():
    """
    Setup the package fixture.
    """
    Config.setup()

def teardown_package():
    """
    Teardown the package fixture.
    """
    Config.teardown()

