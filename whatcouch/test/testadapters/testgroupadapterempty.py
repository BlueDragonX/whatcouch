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
from whatcouch.adapters import GroupAdapter

class TestGroupAdapterEmpty:
    """
    Test the group adapter against an empty database.
    """

    @staticmethod
    def setup_class():
        """
        Create the group adapter.
        """
        Config.adapter = GroupAdapter(Config.t11)

    @staticmethod
    def teardown_class():
        """
        Delete the group adapter.
        """
        del Config.adapter

    def test_get_all_sections(self):
        """
        Test the GroupAdapter._get_all_sections() method.
        """
        sections = Config.adapter._get_all_sections()
        assert type(sections) == dict
        assert len(sections) == 0

    def test_get_section_items(self):
        """
        Test the GroupAdapter._get_section_items() method.
        """
        section = 'nogroup'
        items = Config.adapter._get_section_items(section)
        assert type(items) == list
        assert len(items) == 0

    def test_find_sections(self):
        """
        Test the GroupAdapter._find_sections() method.
        """
        username = 'nouser'
        hint = {'repoze.what.userid': username}
        sections = Config.adapter._find_sections(hint)
        assert type(sections) == list
        assert len(sections) == 0

    def test_item_is_included(self):
        """
        Test the GroupAdapter._item_is_included() method.
        """
        assert Config.adapter._item_is_included('nogroup', 'nouser') == False

    def test_include_items(self):
        """
        Test the GroupAdapter._include_items() method.
        """
        try:
            Config.adapter._include_items('nogroup', ['nouser'])
        except:
            assert False

    def test_edit_section(self):
        """
        Test GroupAdapter._edit_section().
        """
        try:
            Config.adapter._edit_section('oldnogroup', 'newnogroup')
        except:
            assert False

    def test_delete_section(self):
        """
        Test GroupAdapter._delete_section().
        """
        try:
            Config.adapter._delete_section('nogroup')
        except Exception, e:
            print e
            assert False

