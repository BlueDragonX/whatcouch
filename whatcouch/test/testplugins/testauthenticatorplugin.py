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
from whatcouch.plugins import AuthenticatorPlugin

class TestAuthenticatorPlugin:

    @staticmethod
    def setup_class():
        Config.username = 'admin'
        Config.password = 'password'
        Config.user = User.create(Config.username, Config.password)
        Config.user.save()
        Config.plugin = AuthenticatorPlugin(Config.t11)

    @staticmethod
    def teardown_class():
        Config.user.delete()
        del Config.username
        del Config.password
        del Config.user
        del Config.plugin

    def test_authenticate__success(self):
        identity = {'login': Config.username, 'password': Config.password}
        username = Config.plugin.authenticate(Config.environ, identity)
        assert username == Config.username

    def test_authenticate__baduser(self):
        identity = {'login': 'nobody', 'password': Config.password}
        username = Config.plugin.authenticate(Config.environ, identity)
        assert username is None
        
    def test_authenticate__baduser(self):
        identity = {'login': Config.username, 'password': 'nopass'}
        username = Config.plugin.authenticate(Config.environ, identity)
        assert username is None
        
    def test_authenticate__badeverything(self):
        identity = {'login': 'nobody', 'password': 'nopass'}
        username = Config.plugin.authenticate(Config.environ, identity)
        assert username is None

