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

from whatcouch.test import Config
from whatcouch.model import User
from whatcouch.plugins import MetadataPlugin

class TestMetadataPlugin:

    @staticmethod
    def setup_class():
        Config.username = 'admin'
        Config.user = User.create(Config.username, 'password')
        Config.user.save()
        Config.plugin = MetadataPlugin(Config.t11)

    @staticmethod
    def teardown_class():
        Config.user.delete()
        del Config.user
        del Config.plugin

    def test_add_metadata__success(self):
        identity = {'repoze.who.userid': Config.username}
        Config.plugin.add_metadata(Config.environ, identity)
        assert 'user' in identity
        assert identity['user'].username == Config.username

    def test_add_metadata__badid(self):
        identity = {'repoze.who.userid': 'nobody'}
        Config.plugin.add_metadata(Config.environ, identity)
        assert 'user' not in identity

    def test_add_metadata__noid(self):
        identity = {}
        Config.plugin.add_metadata(Config.environ, identity)
        assert 'user' not in identity

