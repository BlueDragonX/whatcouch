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
from whatcouch.model import init_model, User
from whatcouch.quickstart import default_translations

def setup_package():
    User.set_db(Config.db)
    Config.environ = {}
    Config.t11 = default_translations
    Config.t11['user_class'] = User

def teardown_package():
    User.set_db(None)
    del Config.environ
    del Config.t11

