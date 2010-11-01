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
    
