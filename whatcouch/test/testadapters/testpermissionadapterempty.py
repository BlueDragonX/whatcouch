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

