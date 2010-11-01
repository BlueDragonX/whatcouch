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

from couchdbkit.resource import ResourceNotFound
from whatcouch.test import Config
from whatcouch.adapters import GroupAdapter
from whatcouch.model import User, Group

class TestGroupAdapterPopulated:
    """
    Test the group adapter against a populated database.
    """

    @staticmethod
    def setup_class():
        """
        Create the group adapter, load groups and users into the test
        database, and save expected values in the configuration.
        """
        Config.adapter = GroupAdapter(Config.t11)
        g1 = Group(name='g1')   # will have multiple users
        g2 = Group(name='g2')   # will have one user
        g3 = Group(name='g3')   # will have no users
        Config.groups = [g1, g2, g3]
        Group.bulk_save(Config.groups)
        u1 = User(username='u1')    # belongs to g1, g2
        u2 = User(username='u2')    # belongs to g1
        u3 = User(username='u3')    # belongs to no groups
        u1.groups.append(g1)
        u1.groups.append(g2)
        u2.groups.append(g1)
        Config.users = [u1, u2, u3]
        User.bulk_save(Config.users)
        Config.sections = {
            u'g1': [u'u1', u'u2'],
            u'g2': [u'u1'],
            u'g3': []}
        Config.items = {
            u'u1': [u'g1', u'g2'],
            u'u2': [u'g1'],
            u'u3': []}

    @staticmethod
    def teardown_class():
        """
        Delete the users and users from the database and delete the attributes
        added to the configuration.
        """
        for user in Config.users:
            try:
                user.delete()
            except ResourceNotFound:
                pass
        for group in Config.groups:
            try:
                group.delete()
            except ResourceNotFound:
                pass
        del Config.users
        del Config.groups
        del Config.sections
        del Config.items
        del Config.adapter

    def test_get_user__found(self):
        """
        Test GroupAdapter._get_user() for an existing user.
        """
        username = 'u1'
        user = Config.adapter._get_user(username)
        assert user is not None
        assert isinstance(user, User)
        assert user.username == username

    def test_get_user__notfound(self):
        """
        Test GroupAdapter._get_user() for a nonexistent user.
        """
        username = 'nouser'
        user = Config.adapter._get_user(username)
        assert user is None

    def test_get_group__found(self):
        """
        Test GroupAdapter._get_group() for an existing group.
        """
        groupname = 'g1'
        group = Config.adapter._get_group(groupname)
        assert group is not None
        assert isinstance(group, Group)
        assert group.name == groupname

    def test_get_group__notfound(self):
        """
        Test GroupAdapter._get_group() for a nonexistent group.
        """
        groupname = 'nogroup'
        group = Config.adapter._get_group(groupname)
        assert group is None

    def test_get_all_sections(self):
        """
        Test GroupAdapter._get_all_sections().
        """
        u1 = Config.adapter._get_user('u1')
        sections = Config.adapter._get_all_sections()
        assert type(sections) == dict
        assert len(sections) == len(Config.sections)
        for section, items in sections.iteritems():
            assert section in Config.sections
            eitems = Config.sections[section]
            assert type(items) == list
            assert len(items) == len(eitems)
            for item in items:
                assert item in eitems

    def _get_section_items(self, section):
        """
        Test GroupAdapter._get_section_items() for a given section.
        :param section: The section to test _get_section_items() against.
        """
        items = Config.adapter._get_section_items(section)
        assert type(items) == list
        if section in Config.sections:
            eitems = Config.sections[section]
            assert len(items) == len(eitems)
            for item in items:
                assert item in eitems
        else:
            assert len(items) == 0

    def test_get_section_items__manyfound(self):
        """
        Test GroupAdapter._get_section_items() for a group with multiple users.
        """
        self._get_section_items('g1')

    def test_get_section_items__onefound(self):
        """
        Test GroupAdapter._get_section_items() for a group with one user.
        """
        self._get_section_items('g2')

    def test_get_section_items__notfound(self):
        """
        Test GroupAdapter._get_section_items() for a group with no users.
        """
        self._get_section_items('g3')

    def test_get_section_items__nogroup(self):
        """
        Test GroupAdapter._get_section_items() for a nonexistent group.
        """
        self._get_section_items('nogroup')

    def _find_sections(self, username):
        """
        Test GroupAdapter._find_sections() for the specified username.
        :param username: The username to test _find_sections() against.
        """
        hint = {'repoze.what.userid': username}
        sections = Config.adapter._find_sections(hint)
        assert type(sections) == list
        if username in Config.items:
            esections = Config.items[username]
            assert len(sections) == len(esections)
            for section in sections:
                assert section in esections
        else:
            assert len(sections) == 0

    def test_find_sections__manyfound(self):
        """
        Test GroupAdapter._find_section() for a user with multiple groups.
        """
        self._find_sections('u1')

    def test_find_sections__onefound(self):
        """
        Test GroupAdapter._find_section() for a user with one group.
        """
        self._find_sections('u2')

    def test_find_sections__notfound(self):
        """
        Test GroupAdapter._find_section() for a user with no groups.
        """
        self._find_sections('u3')

    def test_find_sections__nouser(self):
        """
        Test GroupAdapter._find_section() for a nonexistent user.
        """
        self._find_sections('nouser')

    def test_item_is_included__true(self):
        """
        Test GroupAdapter._item_is_included() for a user in the group.
        """
        assert Config.adapter._item_is_included('g1', 'u1') == True

    def test_item_is_included__false(self):
        """
        Test GroupAdapter._item_is_included() for a user not in the group.
        """
        assert Config.adapter._item_is_included('g3', 'u1') == False

    def test_item_is_included__nogroup(self):
        """
        Test GroupAdapter._item_is_included() for a nonexistent group and existing user.
        """
        assert Config.adapter._item_is_included('nogroup', 'u1') == False

    def test_item_is_included__nouser(self):
        """
        Test GroupAdapter._item_is_included() for an existing group and a nonexistent user.
        """
        assert Config.adapter._item_is_included('g1', 'nouser') == False

    def _include_items(self, section, items):
        """
        Test GroupAdapter._include_items() for the given group and users.
        Removes the users after a successful test.
        :param section: The section to test _include_items() against.
        :param items: The items to use when testing _include_items().
        """
        Config.adapter._include_items(section, items)
        users = [ Config.adapter._get_user(item) for item in items ]
        for user in users:
            assert user is not None
            found = False
            for i in range(len(user.groups)-1, -1, -1):
                if user.groups[i].name == section:
                    found = True
                    del user.groups[i]
                    user.save()
            assert found

    def test_include_items__one(self):
        """
        Test GroupAdapter._include_items() when adding one user.
        """
        self._include_items('g3', ['u1'])

    def test_include_items__many(self):
        """
        Test GroupAdapter._include_items() when adding multiple users.
        """
        self._include_items('g3', ['u1', 'u2'])

    def test_include_items__nogroup(self):
        """
        Test GroupAdapter._include_items() for a nonexistent group.
        """
        try:
            Config.adapter._include_items('nogroup', ['u1'])
        except:
            assert False

    def test_include_items__nouser(self):
        """
        Test GroupAdapter._include_items() for a nonexistent user.
        """
        try:
            Config.adapter._include_items('g3', ['nouser'])
        except:
            assert False

    def _exclude_items(self, section, items):
        """
        Test GroupAdapter._exclude_items() for the given group and users.
        :param section: The section to test _exclude_items() against.
        :param items: The items to use when testing _exclude_items().
        """
        Config.adapter._exclude_items(section, items)
        group = Config.adapter._get_group(section)
        users = [ Config.adapter._get_user(item) for item in items ]
        found_any = False
        for user in users:
            assert user is not None
            found = False
            for cgroup in user.groups:
                if cgroup.name == section:   
                    found = True
            if not found:
                user.groups.append(group)
            else:
                found_any = True
        User.bulk_save(users)
        assert not found

    def test_exclude_items__one(self):
        """
        Test GroupAdapter._exclude_items() for one user.
        """
        self._exclude_items('g1', ['u1'])

    def test_exclude_items__many(self):
        """
        Test GroupAdapter._exclude_items() for multiple users.
        """
        self._exclude_items('g1', ['u1', 'u2'])

    def test_exclude_items__nogroup(self):
        """
        Test GroupAdapter._exclude_items() for a nonexistent group.
        """
        try:
            Config.adapter._exclude_items('nogroup', ['u1'])
        except:
            assert False

    def test_exclude_items__nouser(self):
        """
        Test GroupAdapter._exclude_items() for a nonexistent user.
        """
        try:
            Config.adapter._exclude_items('g1', ['nouser'])
        except:
            assert False

    def test_section_exists__true(self):
        """
        Test GroupAdapter._section_exists() for an existing group.
        """
        assert Config.adapter._section_exists('g1')

    def test_section_exists__false(self):
        """
        Test GroupAdapter._section_exists() for a nonexistent group.
        """
        assert not Config.adapter._section_exists('nogroup')

    def test_create_section(self):
        """
        Test GroupAdapter._create_section().
        """
        section = 'newgroup'
        Config.adapter._create_section(section)
        group = Config.adapter._get_group(section)
        assert group is not None
        group.delete()

    def test_edit_section(self):
        """
        Test GroupAdapter._edit_section().
        """
        old_section = 'oldgroup'
        new_section = 'newgroup'
        group = Group(name=old_section)
        group.save()
        Config.adapter._edit_section(old_section, new_section)
        new_group = Config.adapter._get_group(new_section)
        assert new_group is not None
        assert new_group.name == new_section
        new_group.delete()

    def test_delete_section(self):
        """
        Test GroupAdapter._delete_section().
        """
        section = 'delgroup'
        group = Group(name=section)
        group.save()
        Config.adapter._delete_section(section)
        del_group = Config.adapter._get_group(section)
        assert del_group is None

