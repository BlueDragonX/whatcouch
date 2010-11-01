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

