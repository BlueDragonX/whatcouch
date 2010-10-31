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
from whatcouch.model import Group

class TestModelGroup:
    """
    Test the group model document.
    """

    def test_subclass(self):
        """
        Verify that Group subclasses couchdbkit.Document.
        """
        assert issubclass(Group, couchdbkit.Document)

