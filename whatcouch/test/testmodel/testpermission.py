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
from whatcouch.model import Permission

class TestModelPermission:
    """
    Test the permission model document.
    """

    def test_subclass(self):
        """
        Verify that Permission subclasses couchdbkit.Document.
        """
        assert issubclass(Permission, couchdbkit.Document)

