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
Tests the repoze.what adapters.
"""

from whatcouch.test import Config
from whatcouch.model import init_model, User, Group, Permission
from whatcouch.quickstart import default_translations

def setup_package():
    """
    Configure the test package for adapter testing.  Assigns the test
    database to the Couch documents and sets up the translations
    dict.
    """
    User.set_db(Config.db)
    Group.set_db(Config.db)
    Permission.set_db(Config.db)
    Config.t11 = default_translations
    Config.t11['user_class'] = User
    Config.t11['group_class'] = Group
    Config.t11['perm_class'] = Permission

def teardown_package():
    """
    Unsets the test database in the Couch documents and unsets the
    translations dict.
    """
    User.set_db(None)
    Group.set_db(None)
    Permission.set_db(None)
    del Config.t11

