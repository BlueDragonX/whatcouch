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
from whatcouch.adapters import PermissionAdapter

class TestPermissionAdapterEmpty:
    """
    Test the permission adapter against an empty database.
    """

    @staticmethod
    def setup_class():
        """
        Create the permission adapter.
        """
        Config.adapter = PermissionAdapter(Config.t11)

    @staticmethod
    def teardown_class():
        """
        Delete the permission adapter.
        """
        del Config.adapter

    def test_get_all_sections(self):
        """
        Test PermissionAdapter._get_all_sections().
        """
        sections = Config.adapter._get_all_sections()
        assert type(sections) == dict
        assert len(sections) == 0

    def test_get_section_items(self):
        """
        Test PermissionAdapter._get_section_items().
        """
        section = 'noperm'
        items = Config.adapter._get_section_items(section)
        assert type(items) == list
        assert len(items) == 0

    def test_find_sections(self):
        """
        Test PermissionAdapter._find_sections().
        """
        hint = 'nogroup'
        sections = Config.adapter._find_sections(hint)
        assert type(sections) == list
        assert len(sections) == 0

    def test_item_is_included(self):
        """
        Test PermissionAdapter._item_is_included().
        """
        assert Config.adapter._item_is_included('noperm', 'nogroup') == False

    def test_include_items(self):
        """
        Test PermissionAdapter._include_items().
        """
        try:
            Config.adapter._include_items('noperm', ['nogroup'])
        except:
            assert False

    def test_edit_section(self):
        """
        Test PermissionAdapter._edit_section().
        """
        try:
            Config.adapter._edit_section('oldnoperm', 'newnoperm')
        except:
            assert False

    def test_delete_section(self):
        """
        Test PermissionAdapter._delete_section().
        """
        try:
            Config.adapter._delete_section('noperm')
        except Exception, e:
            print e
            assert False

