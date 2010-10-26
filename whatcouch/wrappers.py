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
This module contains wrapper classes which are used to map calls to CouchDB
documents.  This mapping is controlled by the translations dict which is
passed to the source adapters, plugins, and quickstart function.  The wrapper
classes should never need to be accessed directly.

The following table documents the supported key values in the translations
dict and each key's purpose:

user_class:             The class for User documents.  Not used by quickstart.
user_name_key:          User attribute where the login name is stored.
user_groups_key:        User attribute where the groups collection is stored.
user_find_by_name:      User static method to retrieve a user by name.
user_find_by_group:     User static method to retrieve a collection of users by group.
user_authenticate:      User method which uses a password to authenticate the user.
group_class:            The class for Group documents.  Not used by quickstart.
group_name_key:         Group attribute where the group name is stored.
group_perms_key:        Group attribute where the permissions collection is stored.
group_list:             Group static method to retrieve all groups.
group_find_by_name:     Group static method to retrieve a group by name.
group_find_by_perm:     Group static method to retrieve a collection of groups by permission.
perm_class:             The class for Permission documents.  Not used by quickstart.
perm_name_key:          Permission attribute where the permission name is stored.
perm_list:              Permission static method to retrieve all permissions.
perm_find_by_name:      Permission static method to retrieve a permission by name.
perm_find_by_group:     Permission static method to retrieve a collection of permissions by group.
"""

class InstanceWrapper:
    """
    Wraps a document object.
    """

    def __init__(self, instance, t11, t11_name_key):
        """
        Constructor.  Create a new wrapper around a document object.
        :param instance: The document object to wrap.
        :param t11: The translations dict to use for this wrapper.
        :param t11_name_key: This tells which key in the translations dict to use when looking up the document object's name.
        """
        self.instance = instance
        self.t11 = t11
        self.t11_name_key = t11_name_key

    @property
    def name(self):
        """
        Property getter for name.  Returns the value of the mapped name attribute.
        :return: The value of the mapped name attribute for the document.
        """
        return getattr(self.instance, self.t11[self.t11_name_key])

    @name.setter
    def name(self, value):
        """
        Property setter for name.  Sets the value of the mapped name attribute.
        :param value: The new value for the mapped name attribute.
        """
        setattr(self.instance, self.t11[self.t11_name_key], value)

    def save(self):
        """
        Save the document object.
        """
        self.instance.save()

    def delete(self):
        """
        Delete the document object.
        """
        self.instance.delete()

class ClassWrapper:
    """
    Wraps a document class.
    """

    def __init__(self, instance_class, instance_wrapper, t11, t11_find_by_name_key):
        """
        Constructor.  Create a new wrapper around a document class.
        :param instance_class: The class of the document.
        :param instance_wrapper: The class of the instance wrapper to use for instances of the class.
        :param t11: The translations dict to use for this wrapper.
        :param t11_find_by_name_key: This tells which key in the translations dict to use when looking up the class's find_by_name method.
        """
        self.t11 = t11
        self.t11_find_by_name_key = t11_find_by_name_key
        self.cls = instance_class
        self.instance_wrapper = instance_wrapper

    def wrap(self, item):
        """
        Wrap a document in an InstanceWrapper.
        :param item: The document to wrap.
        :return: An InstanceWrapper object wrapping the given document.
        """
        if item is None:
            return None
        else:
            return self.instance_wrapper(item, self.t11)

    def wrap_list(self, items):
        """
        Wrap a list of document.  Calls wrap() on each item in the given collection.
        :param items: A collection of items to wrap.
        :return: The resulting collection of wrapped items.
        """
        if items is None:
            return []
        else:
            return [ self.wrap(item) for item in items ]

    def unwrap(self, wrapped):
        """
        Unwrap one or more wrapped items.
        :param wrapped: An InstanceWrapper object or collection of InstanceWrapper objects to unwrap.
        :return: The unwrapped object or list of unwrapped objects, depending on what was passed to the method.
        """
        if type(wrapped) == list:
            return [ item.instance for item in wrapped ]
        else:
            return wrapped.instance

    def get(self, id):
        """
        Look up a document by ID and wrap it.
        :param id: The ID of the document in CouchDB.
        :return: The wrapped document or None if not found.
        """
        return self.wrap(self.cls.get(id))

    def create(self):
        """
        Create a new document, wrap it, and return the resulting InstanceWrapper object.
        :return: An InstanceWrapper object containing the new document.
        """
        return self.wrap(self.cls())

    def bulk_save(self, items):
        """
        Unwraps and bulk-saves a collection of wrapped documents.
        :param items: A collection of wrapped documents to save.
        """
        self.cls.bulk_save(self.unwrap(items))

    def find_by_name(self, name):
        """
        Find a document by name, wrap it in an InstanceWrapper, and return the resulting object.
        :param name: The name of the document to search for.
        :return: An InstanceWrapper object containing the document or None if it can't be found.
        """
        find = getattr(self.cls, self.t11[self.t11_find_by_name_key])
        return self.wrap(find(name))

    def find_by_names(self, names):
        """
        Find a collection of documents by name, wrap them, and return the resulting list.
        :param names: A list containing the names of the documents to search for.
        :return: A list containing all the found documents, each individually wrapped in an InstanceWrapper object.
        """
        find = getattr(self.cls, self.t11[self.t11_find_by_name_key])
        items = [ find(name) for name in names ]
        items = filter(lambda u: u is not None, items)
        return self.wrap_list(items)

class UserClassWrapper(ClassWrapper):
    """
    A class wrapper for User documents.
    """

    def __init__(self, t11):
        """
        Constructor.  Create a new user class wrapper.
        :param t11: The translations to use for the wrapper.
        """
        ClassWrapper.__init__(self, t11['user_class'], UserInstanceWrapper, t11, 'user_find_by_name')

    def find_by_group(self, group_name):
        """
        Search for User documents by group name.
        :param group_name: The name of the group to search by.
        :return: A list of wrapped User documents.
        """
        find = getattr(self.cls, self.t11['user_find_by_group'])
        return self.wrap_list(method(find))

class GroupClassWrapper(ClassWrapper):
    """
    A class wrapper for Group documents.
    """

    def __init__(self, t11):
        """
        Constructor.  Create a new group class wrapper.
        :param t11: The translations to use for the wrapper.
        """
        ClassWrapper.__init__(self, t11['group_class'], GroupInstanceWrapper, t11, 'group_find_by_name')
        self.user_wrapper = UserClassWrapper(t11)

    def list(self):
        """
        Retrieve a list of all groups in the database.
        :return: A list of all groups in the database, individually wrapped.
        """
        ls = getattr(self.cls, self.t11['group_list'])
        return self.wrap_list(ls())

    def find_by_permission(self, name):
        """
        Search for groups with the given permission.
        :param name: The name of the permission to search by.
        :return: A list of wrapped Group documents having the given permission.
        """
        find = getattr(self.cls, self.t11['group_find_by_perm'])
        return self.wrap_list(find(name))

    def find_by_hint(self, hint):
        """
        Search for groups associated with the given hint dict.  Checks for a
        user document in hint['user'] then for a user name in hint['repoze.who.userid'].
        :param hint: A credentials dict.
        """
        user = None
        groups = []
        if 'user' in hint:
            user = self.user_wrapper.wrap(hint['user'])
        elif 'repoze.who.userid' in hint:
            user = self.user_wrapper.find_by_name(hint['repoze.who.userid'])
        if user is not None:
            groups = user.groups
        return groups

class PermissionClassWrapper(ClassWrapper):
    """
    A class wrapper for Permission documents.
    """

    def __init__(self, t11):
        """
        Constructor.  Create a new permission class wrapper.
        :param t11: The translations to use for the wrapper.
        """
        ClassWrapper.__init__(self, t11['perm_class'], PermissionInstanceWrapper, t11, 'perm_find_by_name')

    def list(self):
        """
        Retrieve a list of all permissions in the database.
        :return: A list of all permissions in the database, individually wrapped.
        """
        ls = getattr(self.cls, self.t11['perm_list'])
        return self.wrap_list(ls())

    def find_by_group(self, name):
        """
        Search for permissions assigned to the given group.
        :param name: The name of the group to search by.
        :return: A list of wrapped Permission documents having the given permission.
        """
        find = getattr(self.cls, self.t11['perm_find_by_group'])
        return find(name)
        
class UserInstanceWrapper(InstanceWrapper):
    """
    Wrapper for User document objects.
    """

    def __init__(self, instance, t11):
        """
        Constructor.  Create a new user instance wrapper.
        :param t11: The translations to use for the wrapper.
        """
        InstanceWrapper.__init__(self, instance, t11, 'user_name_key')
        self.group_wrapper = GroupClassWrapper(t11)

    @property
    def groups(self):
        """
        Property getter for groups.  Returns a list of wrapped groups this user is associated with.
        :return: A list of GroupInstanceWrapper objects containing the groups this user is associated with.
        """
        groups = getattr(self.instance, self.t11['user_groups_key'])
        return self.group_wrapper.wrap_list(groups)

    @groups.setter
    def groups(self, value):
        """
        Property setter for groups.  Set the groups this user is associated with.
        :param value: A list of GroupInstanceWrapper objects containing groups this user should be associated with.
        """
        groups = self.group_wrapper.unwrap(value)
        setattr(self.instance, self.t11['user_groups_key'], groups)

    def groups_append(self, groups):
        """
        Append groups to the user.
        :param groups: A list of GroupInstaneWrapper objects containing groups that should be appended to the user.
        """
        instance_groups = getattr(self.instance, self.t11['user_groups_key'])
        instance_groups.append(self.group_wrapper.unwrap(groups))

    def groups_remove(self, names):
        """
        Remove groups from the user.
        :param names: The names of the groups that should be removed from the user.
        """
        instance_groups = getattr(self.instance, self.t11['user_groups_key'])
        groups = self.group_wrapper.unwrap(filter(lambda g: g.name in names, self.groups))
        map(instance_groups.remove, groups)

    def authenticate(self, password):
        """
        Authenticate the user against the given password.
        :param password: The password to authenticate the user with.
        """
        auth = getattr(self.instance, self.t11['user_authenticate'])
        return auth(password)

class GroupInstanceWrapper(InstanceWrapper):
    """
    Wrapper for Group document objects.
    """

    def __init__(self, instance, t11):
        """
        Constructor.  Create a new group instance wrapper.
        :param t11: The translations to use for the wrapper.
        """
        InstanceWrapper.__init__(self, instance, t11, 'group_name_key')
        self.perm_wrapper = PermissionClassWrapper(t11)

    @property
    def permissions(self):
        """
        Property getter for permissions.  Returns a list of wrapped permissions this group contains.
        :return: A list of PermissionInstanceWrapper objects containing the permissions contained in this group.
        """
        perms = getattr(self.instance, self.t11['group_perms_key'])
        return self.perm_wrapper.wrap_list(perms)

    @permissions.setter
    def permissions(self, value):
        """
        Property setter for permissions.  Set the permissions associated with this group.
        :param value: A list of PermissionInstanceWrapper objects containing permissions this user should contain.
        """
        perms = self.perm_wrapper.unwrap(value)
        setattr(self.instance, self.t11['group_perms_key'], perms)

    def permissions_append(self, perms):
        """
        Append permissions to this group.
        :param perms: A list of PermissionInstanceWrapper objects containing the permissions to be appended to this group.
        """
        instance_perms = getattr(self.instance, self.t11['group_perms_key'])
        instance_perms.append(self.perm_wrapper.unwrap(perms))

    def permissions_remove(self, names):
        """
        Remove permissions from a group.
        :param name: A list of permission names to remove from the group.
        """
        instance_perms = getattr(self.instance, self.t11['group_perms_key'])
        perms = self.perm_wrapper.unwrap(filter(lambda p: p.name in names, self.permissions))
        map(instance_perms.remove, perms)

class PermissionInstanceWrapper(InstanceWrapper):
    """
    Wrapper for Permission document objects.
    """

    def __init__(self, instance, t11):
        """
        Constructor.  Create a new permission instance wrapper.
        :param t11: The translations to use for the wrapper.
        """
        InstanceWrapper.__init__(self, t11, 'perm_name_key')

