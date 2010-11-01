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
"""
This module provides the repoze.what source adapters.  For more details see
the repoze.what documentation at <http://what.repoze.org/docs/1.0/>.

The translations dict passed to the constructor of each adapter is used to map
calls to the provided model using the wrapper classes.  See wrapper.py for
documentation on the translations dict.
"""

from repoze.what.adapters import BaseSourceAdapter

__all__ = ['GroupAdapter', 'PermissionAdapter']

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
        self.User = self.t11['user_class']
        self.user_name_key = self.t11['user_name_key']
        self.user_groups_key = self.t11['user_groups_key']
        self.user_list_view = self.t11['user_list_view']
        self.user_by_group_view = self.t11['user_by_group_view']
        self.Group = self.t11['group_class']
        self.group_name_key = self.t11['group_name_key']
        self.group_list_view = self.t11['group_list_view']

    def _get_user(self, name):
        """
        Get a user by name.
        :param name: The name of the user to get.
        :return: The user document with the given name or None if not found.
        """
        users = self.User.view(self.user_list_view, key=name)
        if len(users) > 0:
            return users.__iter__().next()
        return None

    def _get_group(self, name):
        """
        Get a group by name.
        :param name: The name of the group to get.
        :return: The group document with the given name or None if not found.
        """
        groups = self.Group.view(self.group_list_view, key=name)
        if len(groups) > 0:
            return groups.__iter__().next()
        return None

    def _get_all_sections(self):
        """
        Get a dictionary containing all groups.  The keys will be the group names
        and the values will be a list of user names contained in that group.
        :return: A dictionary of group to user name list mappings.
        """
        sections = {}
        groups = self.Group.view(self.group_list_view)
        for group in groups:
            name = getattr(group, self.group_name_key)
            sections[name] = self._get_section_items(name)
        return sections
            
    def _get_section_items(self, section):
        """
        Get a list of user names for the given group.
        :param section: The name of the group to retrieve user names for.
        :return: A list of user names.  Will be empty of the group does not exist.
        """
        users = self.User.view(self.user_by_group_view, key=section)
        return [ getattr(user, self.user_name_key) for user in users ]

    def _find_sections(self, hint):
        """
        Find groups based on the credentials dict.
        :param hint: The credentials dict.
        :return: A list of group names associated with the user found in the credentials dict.
        """
        user = None
        sections = []
        if user in hint:
            user = hint['user']
        elif 'repoze.what.userid' in hint:
            name = hint['repoze.what.userid']
            user = self._get_user(name)
        if user is not None:
            sections = [ getattr(group, self.group_name_key) for group in user.groups ]
        return sections

    def _item_is_included(self, section, item):
        """
        Check if a user belongs to a group.
        :param section: The name of the group to check.
        :param item: The name of the user to check.
        :return: True if the user is in the group, False otherwise.
        """
        user = self._get_user(item)
        if user is not None:
            for group in user.groups:
                if getattr(group, self.group_name_key) == section:
                    return True
        return False

    def _include_items(self, section, items):
        """
        Add users to a group.
        :param section: The name of the group to add the users to.
        :param items: A list containing names of users to add to the group.
        """
        group = self._get_group(section)
        if group is not None:
            save_users = []
            for item in items:
                user = self._get_user(item)
                if user is not None:
                    getattr(user, self.user_groups_key).append(group)
                    save_users.append(user)
            self.User.bulk_save(save_users)

    def _exclude_items(self, section, items):
        """
        Remove users from a group.
        :param section: The name of the group to remove users from.
        :param items: A list containing names of users to remove from the group.
        """
        save_users = []
        for item in items:
            user = self._get_user(item)
            if user is not None:
                add_user = False
                groups = getattr(user, self.user_groups_key)
                for i in range(len(groups)-1, -1, -1):
                    if getattr(groups[i], self.group_name_key) == section:
                        del groups[i]
                        add_user = True
                if add_user:
                    save_users.append(user)
        self.User.bulk_save(save_users)

    def _section_exists(self, section):
        """
        Check if a group exists.
        :param section: The name of the group to check.
        :return: True if the group exists, False otherwise.
        """
        return len(self.Group.view(self.group_list_view, key=section)) > 0

    def _create_section(self, section):
        """
        Create a new group.
        :param section: The name of the new group.
        """
        group = self.Group()
        setattr(group, self.group_name_key, section)
        group.save()

    def _edit_section(self, section, new_section):
        """
        Edit a group name.
        :param section: The name of the group to change.
        :param new_section: The new name of the group.
        """
        group = self._get_group(section)
        if group is not None:
            setattr(group, self.group_name_key, new_section)
            group.save()

    def _delete_section(self, section):
        """
        Delete the group.
        :param section: The name of the group to delete.
        """
        group = self._get_group(section)
        if group is not None:
            save_users = []
            users = self.User.view(self.user_by_group_view, key=section)
            for user in users:
                add_user = False
                groups = getattr(user, self.user_groups_key)
                for i in range(len(groups)-1, -1, -1):
                    if getattr(groups[i], self.group_name_key) == section:
                        del groups[i]
                        add_user = True
                if add_user:
                    save_users.append(user)
            self.User.bulk_save(save_users)
            group.delete()

class PermissionAdapter(BaseSourceAdapter):

    def __init__(self, translations):
        """
        Constructor.  Configures the adapter with the given translations dict.
        :param translations: The translations to use when mapping requests against a model.
        """
        self.t11 = translations
        self.Group = self.t11['group_class']
        self.group_name_key = self.t11['group_name_key']
        self.group_perms_key = self.t11['group_perms_key']
        self.group_list_view = self.t11['group_list_view']
        self.group_by_perm_view = self.t11['group_by_perm_view']
        self.Permission = self.t11['perm_class']
        self.perm_name_key = self.t11['perm_name_key']
        self.perm_list_view = self.t11['perm_list_view']
        self.perm_by_group_view = self.t11['perm_by_group_view']

    def _get_group(self, name):
        """
        Get a group by name.
        :param name: The name of the group to get.
        :return: The named group document or None if not found.
        """
        groups = self.Group.view(self.group_list_view, key=name)
        if len(groups) > 0:
            return groups.__iter__().next()
        return None

    def _get_perm(self, name):
        """
        Get a permission by name.
        :param name: The name of the permission to get.
        :return: The named permission document or None if not found.
        """
        perms = self.Permission.view(self.perm_list_view, key=name)
        if len(perms) > 0:
            return perms.__iter__().next()
        return None

    def _get_all_sections(self):
        """
        Get a dictionary containing all permissions.  The keys will be the permission
        names and the values will be a list of group names contained in that permission.
        :return: A dictionary of permission to group name list mappings.
        """
        sections = {}
        perms = self.Permission.view(self.perm_list_view)
        for perm in perms:
            name = getattr(perm, self.perm_name_key)
            sections[name] = self._get_section_items(name)
        return sections

    def _get_section_items(self, section):
        """
        Get a list of group names for the given permission.
        :param section: The name of the permission to retrieve group names for.
        :return: A list of group names.  Will be empty of the permission does not exist.
        """
        groups = self.Group.view(self.group_by_perm_view, key=section)
        return [ getattr(group, self.group_name_key) for group in groups ]

    def _find_sections(self, hint):
        """
        Retrieve permissions containing a particular group.
        :param hint: The group name to retrieve permissions for.
        """
        perms = self.Permission.view(self.perm_by_group_view, key=hint)
        return [ getattr(perm, self.perm_name_key) for perm in perms ]

    def _item_is_included(self, section, item):
        """
        Check if a group belongs to a permission.
        :param section: The name of the permission to check.
        :param item: The name of the group to check.
        :return: True if the group is in the permission, False otherwise.
        """
        group = self._get_group(item)
        if group is not None:
            for perm in getattr(group, self.group_perms_key):
                if getattr(perm, self.perm_name_key) == section:
                    return True
        return False

    def _include_items(self, section, items):
        """
        Add groups to a permission.
        :param section: The name of the permission to add the groups to.
        :param items: A list containing names of groups to add to the permission.
        """
        perm = self._get_perm(section)
        if perm is not None:
            save_groups = []
            for item in items:
                group = self._get_group(item)
                if group is not None:
                    getattr(group, self.group_perms_key).append(perm)
                    save_groups.append(group)
            self.Group.bulk_save(save_groups)

    def _exclude_items(self, section, items):
        """
        Remove groups from a permission.
        :param section: The name of the permission to remove groups from.
        :param items: A list containing names of groups to remove from the permission.
        """
        save_groups = []
        for item in items:
            group = self._get_group(item)
            if group is not None:
                add_group = False
                perms = getattr(group, self.group_perms_key)
                for i in range(len(perms)-1, -1, -1):
                    if getattr(perms[i], self.perm_name_key) == section:
                        del perms[i]
                        add_group = True
                if add_group:
                    save_groups.append(group)
        self.Group.bulk_save(save_groups)

    def _section_exists(self, section):
        """
        Check if a permission exists.
        :param section: The name of the permission to check.
        :return: True if the permission exists, False otherwise.
        """
        return len(self.Permission.view(self.perm_list_view, key=section)) > 0

    def _create_section(self, section):
        """
        Create a new permission.
        :param section: The name of the new permission.
        """
        perm = self.Permission()
        setattr(perm, self.perm_name_key, section)
        perm.save()

    def _edit_section(self, section, new_section):
        """
        Edit a permission name.
        :param section: The name of the permission to change.
        :param new_section: The new name of the permission.
        """
        perm = self._get_perm(section)
        if perm is not None:
            setattr(perm, self.perm_name_key, new_section)
            perm.save()

    def _delete_section(self, section):
        """
        Delete the permission.
        :param section: The name of the permission to delete.
        """
        perm = self._get_perm(section)
        if perm is not None:
            save_groups = []
            groups = self.Group.view(self.group_by_perm_view, key=section)
            for group in groups:
                add_group = False
                perms = getattr(group, self.group_perms_key)
                for i in range(len(perms)-1, -1, -1):
                    if getattr(perms[i], self.perm_name_key) == section:
                        del perms[i]
                        add_group = True
                if add_group:
                    save_groups.append(group)
            self.Group.bulk_save(save_groups)
            perm.delete()

