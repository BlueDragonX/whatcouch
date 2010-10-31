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

