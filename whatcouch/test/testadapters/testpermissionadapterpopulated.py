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

from couchdbkit.resource import ResourceNotFound
from whatcouch.test import Config
from whatcouch.adapters import PermissionAdapter
from whatcouch.model import Group, Permission

class TestPermissionAdapterPopulated:
    """
    Test the permission adapter against a populated database.
    """

    @staticmethod
    def setup_class():
        """
        Create the permission adapter, add permissions and groups to the
        database, and add expected values to the configuration.
        """
        Config.adapter = PermissionAdapter(Config.t11)
        p1 = Permission(name='p1')   # will have multiple groups
        p2 = Permission(name='p2')   # will have one groups
        p3 = Permission(name='p3')   # will have no group
        Config.perms = [p1, p2, p3]
        Permission.bulk_save(Config.perms)
        g1 = Group(name='g1')    # belongs to p1, p2
        g2 = Group(name='g2')    # belongs to p1
        g3 = Group(name='g3')    # belongs to no groups
        g1.permissions.append(p1)
        g1.permissions.append(p2)
        g2.permissions.append(p1)
        Config.groups = [g1, g2, g3]
        Group.bulk_save(Config.groups)
        Config.sections = {
            'p1': ['g1', 'g2'],
            'p2': ['g1'],
            'p3': []}
        Config.items = {
            'g1': ['p1', 'p2'],
            'g2': ['p1'],
            'g3': []}

    @staticmethod
    def teardown_class():
        """
        Delete permissions and groups from the database and delete
        configured attributes from the config.
        """
        for group in Config.groups:
            try:
                group.delete()
            except ResourceNotFound:
                pass
        for perm in Config.perms:
            try:
                perm.delete()
            except ResourceNotFound:
                pass
        del Config.groups
        del Config.perms
        del Config.sections
        del Config.items
        del Config.adapter

    def test_get_group__found(self):
        """
        Test PermissionAdapter._get_group() for an existing group.
        """
        groupname = 'g1'
        group = Config.adapter._get_group(groupname)
        assert group is not None
        assert isinstance(group, Group)
        assert group.name == groupname

    def test_get_group__notfound(self):
        """
        Test PermissionAdapter._get_group() for a nonexistent group.
        """
        groupname = 'g4'
        group = Config.adapter._get_group(groupname)
        assert group is None

    def test_get_perm__found(self):
        """
        Test PermissionAdapter._get_perm() for an existing permission.
        """
        permname = 'p1'
        perm = Config.adapter._get_perm(permname)
        assert perm is not None
        assert isinstance(perm, Permission)
        assert perm.name == permname

    def test_get_perm__notfound(self):
        """
        Test PermissionAdapter._get_perm() for a nonexistent permission.
        """
        permname = 'noperm'
        perm = Config.adapter._get_perm(permname)
        assert perm is None

    def test_get_all_sections(self):
        """
        Test PermissionAdapter._get_all_sections().
        """
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
        Test PermissionAdapter._get_section_items() for the given permission.
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
        Test PermissionAdapter._get_section_items() for a permission with
        multiple groups.
        """
        self._get_section_items('p1')

    def test_get_section_items__onefound(self):
        """
        Test PermissionAdapter._get_section_items() for a permission with
        one groups.
        """
        self._get_section_items('p2')

    def test_get_section_items__notfound(self):
        """
        Test PermissionAdapter._get_section_items() for a permission
        with no groups.
        """
        self._get_section_items('p3')

    def test_get_section_items__noperm(self):
        """
        Test PermissionAdapter._get_section_items() for a nonexistent
        permission.
        """
        self._get_section_items('noperm')

    def _find_sections(self, group):
        """
        Test PermissionAdapter._find_sections() for a given group.
        :param group: The group to test _find_sections() against.
        """
        sections = Config.adapter._find_sections(group)
        assert type(sections) == list
        if group in Config.items:
            esections = Config.items[group]
            assert len(sections) == len(esections)
            for section in sections:
                assert section in esections
        else:
            assert len(sections) == 0

    def test_find_sections__manyfound(self):
        """
        Test PermissionAdapter._find_sections() for a permission with
        multiple groups.
        """
        self._find_sections('g1')

    def test_find_sections__onefound(self):
        """
        Test PermissionAdapter._find_sections() for a permission with one
        group.
        """
        self._find_sections('g2')

    def test_find_sections__notfound(self):
        """
        Test PermissionAdapter._find_sections() for a permission with no
        groups.
        """
        self._find_sections('g3')

    def test_find_sections__nogroup(self):
        """
        Test PermissionAdapter._find_sections() for a nonexistent permission.
        """
        self._find_sections('nogroup')

    def test_item_is_included__true(self):
        """
        Test PermissionAdapter._item_is_included() for a permission containing
        the group.
        """
        assert Config.adapter._item_is_included('p1', 'g1') == True

    def test_item_is_included__false(self):
        """
        Test PermissionAdapter._item_is_included() for a permission not
        containing the group.
        """
        assert Config.adapter._item_is_included('p3', 'g1') == False

    def test_item_is_included__noperm(self):
        """
        Test PermissionAdapter._item_is_included() for a nonexistent permission
        and an existing group.
        """
        assert Config.adapter._item_is_included('noperm', 'g1') == False

    def test_item_is_included__nogroup(self):
        """
        Test PermissionAdapter._item_is_included for an existing permission
        and a nonexistent group.
        """
        assert Config.adapter._item_is_included('p1', 'nogroup') == False

    def _include_items(self, section, items):
        """
        Test PermissionAdapter._include_items() for a given section and items.
        :param section: The permission to test _include_items() against.
        :param items: The groups to test _include_items() against.
        """
        Config.adapter._include_items(section, items)
        groups = [ Config.adapter._get_group(item) for item in items ]
        for group in groups:
            assert group is not None
            found = False
            for i in range(len(group.permissions)-1, -1, -1):
                if group.permissions[i].name == section:
                    found = True
                    del group.permissions[i]
                    group.save()
            assert found

    def test_include_items__one(self):
        """
        Test PermissionAdapter._include_items() with one group.
        """
        self._include_items('p3', ['g1'])

    def test_include_items__many(self):
        """
        Test PermissionAdapter._include_items() with multiple groups.
        """
        self._include_items('p3', ['g1', 'g2'])

    def test_include_items__noperm(self):
        """
        Test PermissionAdapter._include_items() with a nonexistent permission.
        """
        try:
            Config.adapter._include_items('noperm', ['g1'])
        except:
            assert False

    def test_include_items__nogroup(self):
        """
        Test PermissionAdapter._include_items() with a nonexistent group.
        """
        try:
            Config.adapter._include_items('p3', ['nogroup'])
        except:
            assert False

    def _exclude_items(self, section, items):
        """
        Test PermissionAdapter._exclude_items() against the given permission and groups.
        :param section: The permission to test _exclude_items() against.
        :param items: The groups to test _exclude_items() against.
        """
        Config.adapter._exclude_items(section, items)
        perm = Config.adapter._get_perm(section)
        groups = [ Config.adapter._get_group(item) for item in items ]
        found_any = False
        for group in groups:
            found = False
            for cperm in group.permissions:
                if cperm.name == section:
                    found = True
            if not found:
                print '%s -> %s' % (group.name, perm.name)
                group.permissions.append(perm)
            else:
                found_any = True
        Group.bulk_save(groups)
        assert not found

    def test_exclude_items__one(self):
        """
        Test PermissionAdapter._exclude_items() with one group.
        """
        self._exclude_items('p1', ['g1'])

    def test_exclude_items__many(self):
        """
        Test PermissionAdapter._exclude_items() with multiple groups.
        """
        self._exclude_items('p1', ['g1', 'g2'])

    def test_exclude_items__noperm(self):
        """
        Test PermissionAdapter._exclude_items() with a nonexistent permission.
        """
        try:
            Config.adapter._exclude_items('noperm', ['g1'])
        except:
            assert False

    def test_exclude_items__nogroup(self):
        """
        Test PermissionAdapter._exclude_items() with a nonexistent group.
        """
        try:
            Config.adapter._exclude_items('p1', ['nogroup'])
        except:
            assert False

    def test_section_exists__true(self):
        """
        Test PermissionAdapter._section_exists() against an existing
        permission.
        """
        assert Config.adapter._section_exists('p1')

    def test_section_exists__false(self):
        """
        Test PermissionAdapter._section_exists() against a nonexistent
        permission.
        """
        assert not Config.adapter._section_exists('noperm')

    def test_create_section(self):
        """
        Test PermissionAdapter._create_section().
        """
        section = 'newperm'
        Config.adapter._create_section(section)
        perm = Config.adapter._get_perm(section)
        assert perm is not None
        perm.delete()

    def test_edit_section(self):
        """
        Test PermissionAdapter._edit_section().
        """
        old_section = 'oldperm'
        new_section = 'newperm'
        perm = Permission(name=old_section)
        perm.save()
        Config.adapter._edit_section(old_section, new_section)
        new_perm = Config.adapter._get_perm(new_section)
        assert new_perm is not None
        assert new_perm.name == new_section
        new_perm.delete()

    def test_delete_section(self):
        """
        Test PermissionAdapter._delete_section().
        """
        section = 'delperm'
        perm = Permission(name=section)
        perm.save()
        Config.adapter._delete_section(section)
        del_perm = Config.adapter._get_perm(section)
        assert del_perm is None

