# Copyright (c) 2010, Ryan Bourgeois <bluedragonx@gmail.com>
# All rights reserved.
#
# This software is licensed under the GNU General Public License v2.0.
# A copy of the license should have been included with this file but
# is available online at http://www.gnu.org/licenses/gpl-2.0.html.
# This software is provided "as is" and any and all express or implied
# warranties are disclaimed, including, but not limited to, the implied
# warranties of title, merchantability, against infringement, and fitness
# for a particular purpose.
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

