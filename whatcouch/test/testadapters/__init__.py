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

