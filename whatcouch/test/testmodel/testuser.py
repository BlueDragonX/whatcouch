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

import couchdbkit
from whatcouch.test import Config
from whatcouch.model import User, hashcmp

class TestModelUser:
    """
    Test the user model document.
    """

    @staticmethod
    def setup_class():
        """
        Set the username and password to use for testing.
        """
        Config.username = 'testuser'
        Config.password = 'password'

    @staticmethod
    def teardown_class():
        """
        Delete the username and password from the configuration.
        """
        del Config.username
        del Config.password

    def test_subclass(self):
        """
        Verify that User subclasses couchdbkit.User.
        """
        assert issubclass(User, couchdbkit.Document)

    def test_create(self):
        """
        Test User.create().
        """
        user = User.create(Config.username, Config.password)
        assert user.username == Config.username
        assert hashcmp(user.password, Config.password)

    def test_set_password(self):
        """
        Test User.set_password().
        """
        user = User(username=Config.username)
        user.set_password(Config.password)
        assert hashcmp(user.password, Config.password)

    def test_authenticate(self):
        """
        Test User.authenticate().
        """
        user = User.create(Config.username, Config.password)
        assert user.authenticate(Config.password)
    
