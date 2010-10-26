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
"""
This module provides the repoze.what source adapters.  For more details see
the repoze.what documentation at <http://what.repoze.org/docs/1.0/>.

The translations dict passed to the constructor of each adapter is used to map
calls to the provided model using the wrapper classes.  See wrapper.py for
documentation on the translations dict.
"""

from repoze.what.adapters import BaseSourceAdapter
from whatcouch.wrappers import *

class GroupAdapter(BaseSourceAdapter):
    """
    CouchDB group source adapter.
    """

    def __init__(self, translations):
        """
        Constructor.  Configures the adapter with the given translations dict.
        :param translations: The translations to use when mapping requests against a model.
        """
        self.t11 = translations
        self.user_wrapper = UserClassWrapper(translations)
        self.group_wrapper = GroupClassWrapper(translations)

    def _get_all_sections(self):
        """
        Get a dictionary containing all groups.  The keys will be the group names
        and the values will be a list of user names contained in that group.
        :return: A dictionary of group to user name list mappings.
        """
        sections = {}
        groups = self.group_wrapper.list()
        for group in groups:
            sections[group.name] = self._get_section_items(group.name)
        return sections

    def _get_section_items(self, section):
        """
        Get a list of user names for the given group.
        :param section: The name of the group to retrieve user names for.
        :return: A list of user names.  Will be empty of the group does not exist.
        """
        users = self.user_wrapper.find_by_group(section)
        return [ user.name for user in users ]

    def _find_sections(self, hint):
        """
        Find groups based on the credentials dict.
        :param hint: The credentials dict.
        :return: A list of group names associated with the user found in the credentials dict.
        """
        return [ group.name for group in self.group_wrapper.find_by_hint(hint) ]

    def _item_is_included(self, section, item):
        """
        Check if a user belongs to a group.
        :param section: The name of the group to check.
        :param item: The name of the user to check.
        :return: True if the user is in the group, False otherwise.
        """
        user = self.user_wrapper.find_by_name(item)
        if user is not None:
            for group in user.groups:
                if group.name == section:
                    return True
        return False

    def _include_items(self, section, items):
        """
        Add users to a group.
        :param section: The name of the group to add the users to.
        :param items: A list containing names of users to add to the group.
        """
        group = self.group_wrapper.find_by_name(section)
        if group is not None:
            users = self.user_wrapper.find_by_names(items)
            map(lambda u: u.group_append(group), users)
            self.user_wrapper.bulk_save(users)

    def _exclude_items(self, section, items):
        """
        Remove users from a group.
        :param section: The name of the group to remove users from.
        :param items: A list containing names of users to remove from the group.
        """
        users = self.user_wrapper.find_by_names(items)
        map(lambda u: u.groups_remove([section]))
        self.user_wrapper.bulk_save(users)

    def _section_exists(self, section):
        """
        Check if a group exists.
        :param section: The name of the group to check.
        :return: True if the group exists, False otherwise.
        """
        return self.group_wrapper.find_by_name(section) is not None

    def _create_section(self, section):
        """
        Create a new group.
        :param section: The name of the new group.
        """
        group = self.group_wrapper.create()
        group.name = section
        group.save()

    def _edit_section(self, section, new_section):
        """
        Edit a group name.
        :param section: The name of the group to change.
        :param new_section: The new name of the group.
        """
        group = self.group_wrapper.find_by_name(section)
        if group is not None:
            group.name = new_section
            group.save()

    def _delete_section(self, section):
        """
        Delete the group.
        :param section: The name of the group to delete.
        """
        group = self.group_wrapper.find_by_name(section)
        if group is not None:
            users = self.user_wrapper.find_by_group(section)
            map(lambda u: u.groups_remove([section]), users)
            self.user_wrapper.bulk_save(users)
            group.delete()

class PermissionAdapter(BaseSourceAdapter):

    def __init__(self, translations):
        """
        Constructor.  Configures the adapter with the given translations dict.
        :param translations: The translations to use when mapping requests against a model.
        """
        self.t11 = translations
        self.perm_wrapper = PermissionClassWrapper(translations)
        self.group_wrapper = GroupClassWrapper(translations)

    def _get_all_sections(self):
        """
        Get a dictionary containing all permissions.  The keys will be the permission
        names and the values will be a list of group names contained in that permission.
        :return: A dictionary of permission to group name list mappings.
        """
        sections = {}
        perms = self.perm_wrapper.list()
        for perm in perms:
            sections[perm.name] = self._get_section_items(perm.name)
        return sections

    def _get_section_items(self, section):
        """
        Get a list of group names for the given permission.
        :param section: The name of the permission to retrieve group names for.
        :return: A list of group names.  Will be empty of the permission does not exist.
        """
        groups = self.group_wrapper.find_by_permission(section)
        return [ group.name for group in groups ]

    def _find_sections(self, hint):
        """
        Retrieve permissions containing a particular group.
        :param hint: The group name to retrieve permissions for.
        """
        return [ perm.name for perm in self.perm_wrapper.find_by_group(hint) ]

    def _item_is_included(self, section, item):
        """
        Check if a group belongs to a permission.
        :param section: The name of the permission to check.
        :param item: The name of the group to check.
        :return: True if the group is in the permission, False otherwise.
        """
        group = self.group_wrapper.find_by_name(item)
        if group is not None:
            for perm in group.permissions:
                if perm.name == section:
                    return True
        return False

    def _include_items(self, section, items):
        """
        Add groups to a permission.
        :param section: The name of the permission to add the groups to.
        :param items: A list containing names of groups to add to the permission.
        """
        perm = self.perm_wrapper.find_by_name(section)
        if perm is not None:
            groups = [ self.group_wrapper.find_by_name(item) for item in items ]
            groups = filter(lambda g: g is not None, groups)
            map(lambda g: g.permissions_append(perm), groups)
            self.group_wrapper.bulk_save(groups)

    def _exclude_items(self, section, items):
        """
        Remove groups from a permission.
        :param section: The name of the permission to remove groups from.
        :param items: A list containing names of groups to remove from the permission.
        """
        groups = self.group_wrapper.find_by_names(items)
        map(lambda g: g.permissions_remove([section]))
        self.group_wrapper.bulk_save(groups)

    def _section_exists(self, section):
        """
        Check if a permission exists.
        :param section: The name of the permission to check.
        :return: True if the permission exists, False otherwise.
        """
        return self.perm_wrapper.find_by_name(section) is not None

    def _create_section(self, section):
        """
        Create a new permission.
        :param section: The name of the new permission.
        """
        perm = self.perm_wrapper.create()
        perm.name = section
        perm.save()

    def _edit_section(self, section, new_section):
        """
        Edit a permission name.
        :param section: The name of the permission to change.
        :param new_section: The new name of the permission.
        """
        perm = self.perm_wrapper.find_by_name(section)
        if perm is not None:
            perm.name = new_section
            perm.save()

    def _delete_section(self, section):
        """
        Delete the permission.
        :param section: The name of the permission to delete.
        """
        perm = self.perm_wrapper.find_by_name(section)
        if perm is not None:
            perm.delete()

