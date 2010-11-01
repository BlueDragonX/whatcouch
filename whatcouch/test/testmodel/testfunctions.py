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

import bcrypt
from whatcouch.model import hashpw, hashcmp, init_model, User, Group, Permission
from whatcouch.test import Config

class TestModelFunctions:
    """
    Test the functions in the model.
    """

    @staticmethod
    def setup_class():
        """
        Set the password to use for testing the hash functions.
        """
        Config.password = 'password'

    @staticmethod
    def teardown_class():
        """
        Delete the password attribute and remove the database
        associated with the model documents.
        """
        del Config.password
        User.set_db(None)
        Group.set_db(None)
        Permission.set_db(None)

    def test_hashpw(self):
        """
        Test the hashpw function.
        """
        salt = bcrypt.gensalt()
        hash = bcrypt.hashpw(Config.password, salt)
        assert hash == hashpw(Config.password, salt)

    def test_hashcmp(self):
        """
        Test the hashcmp function.
        """
        hash = hashpw(Config.password)
        assert hashcmp(hash, Config.password)

    def test_init_model(self):
        """
        Test the init_model function.
        """
        init_model(Config.db)
        assert User.get_db() == Config.db
        assert Group.get_db() == Config.db
        assert Permission.get_db() == Config.db

