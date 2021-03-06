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
This module provides a quickstart function similar to that provided by the
repoze.what quickstart plugin.
"""

from repoze.who.plugins.auth_tkt import AuthTktCookiePlugin
from repoze.who.plugins.friendlyform import FriendlyFormPlugin
from repoze.what.middleware import setup_auth
from whatcouch.adapters import GroupAdapter, PermissionAdapter
from whatcouch.plugins import AuthenticatorPlugin, MetadataPlugin
from whatcouch.model import User, Group, Permission

__all__ = ['setup_couch_auth']

"""
Default translations.  These will be substituted for missing values
in the translations dict that is passed to the quickstart function.

The following table documents the supported key values in the translations
dict and each key's purpose:

user_class:             The class for User documents.  Not used by quickstart.
user_name_key:          User attribute where the login name is stored.
user_groups_key:        User attribute where the groups collection is stored.
user_list_view:         The name of a view that maps user names to user documents.
user_by_group_view:     The name of a view that maps group names to user documents.
user_auth_method:       Method on the User document which should be used to authenticate the user.  Takes the password as an argument.
group_class:            The class for Group documents.  Not used by quickstart.
group_name_key:         Group attribute where the group name is stored.
group_perms_key:        Group attribute where the permissions collection is stored.
group_list_view:        The name of a view that maps group names to group documents.
group_by_perm_view:     The name of a view that maps permission names to group documents.
perm_class:             The class for Permission documents.  Not used by quickstart.
perm_name_key:          Permission attribute where the permission name is stored.
perm_list_view:         The name of a view that maps permission names to permission documents.
perm_by_group_view:     The name of a view that maps group names to permission documents.
"""
default_translations = {
    'user_class': None,
    'user_name_key': 'username',
    'user_groups_key': 'groups',
    'user_list_view': 'whatcouch/user_list',
    'user_by_group_view': 'whatcouch/user_by_group',
    'user_auth_method': 'authenticate',
    'group_class': None,    
    'group_name_key': 'name',
    'group_perms_key': 'permissions',
    'group_list_view': 'whatcouch/group_list',
    'group_by_perm_view': 'whatcouch/group_by_permission',
    'perm_class': None,
    'perm_name_key': 'name',
    'perm_list_view': 'whatcouch/permission_list',
    'perm_by_group_view': 'whatcouch/permission_by_group'}

def setup_couch_auth(app, user_class=None, group_class=None, permission_class=None, 
        form_plugin=None, form_identities=True,
        cookie_secret='secret', cookie_name='authtkt', cookie_timeout=None, cookie_reissue_time=None,
        charset='utf-8', login_url='/login', login_handler='/login_handler', post_login_url=None,
        logout_handler='/logout_handler', post_logout_url=None, login_counter_name=None,
        translations=None, **who_args):
    """
    Quickly configure repoze.who and repoze.what to use CouchDB for authentication and authorization.
    With the exception of app, all parameters are options.
    :param app: The WSGI application.
    :param user_class: The class to use for the User document.
    :param group_class: The class to use for the Group document.
    :param permission_class: The class to use for the Permission document.
    :param form_plugin: The form plugin to use.  Defaults to FriendlyFormPlugin.
    :param form_identities: Whether or not to use the form plugin as an identity plugin.
    :param cookie_secret: The cookie secret to use for the authtkt plugin.
    :param cookie_name: The name of the cookie for the authtkt plugin.
    :param cookie_timeout: The cookie timeout for the authtkt plugin.
    :param cookie_reissue_time: How often to reissue the cookie for the authtkt plugin.
    :param charset: The character set for the authtkt plugin.
    :param login_url: The page that will be used to display the login form.
    :param login_handler: The URL where repoze.who will process logins.
    :param post_login_url: The URL to redirect to after login.
    :param logout_handler: The URL where repoze.who will process logouts.
    :param post_logout_url: The URL to redirect to after logout.
    :param login_counter_name: The name to use for the login counter.
    :param translations: The translations used to map CouchDB documents inside the wrapper classes.
    :param who_args: Additional configuration arguments to pass to repoze.who.
    :return: The modified WSGI application.
    """
    t11 = default_translations
    if translations is not None:
        for k, v in translations.iteritems():
            t11[k] = v

    t11['user_class'] = User if user_class is None else user_class
    t11['group_class'] = Group if group_class is None else group_class
    t11['perm_class'] = Permission if permission_class is None else permission_class

    if form_plugin is None:
        form_plugin = FriendlyFormPlugin(login_url, login_handler, post_login_url, logout_handler, post_logout_url,
            login_counter_name=login_counter_name, rememberer_name='cookie', charset=charset)
    group_adapters = {'couch_auth': GroupAdapter(t11)}
    perm_adapters = {'couch_auth': PermissionAdapter(t11)}
    authenticator = ('couch_auth', AuthenticatorPlugin(t11))
    metadata = ('couch_auth', MetadataPlugin(t11))
    identifier = ('cookie', AuthTktCookiePlugin(cookie_secret, cookie_name, timeout=cookie_timeout, reissue_time=cookie_reissue_time))
    challenger = ('form', form_plugin)
    
    if 'authenticators' not in who_args:
        who_args['authenticators'] = []
    if 'identifiers' not in who_args:
        who_args['identifiers'] = []
    if 'challengers' not in who_args:
        who_args['challengers'] = []
    if 'mdproviders' not in who_args:
        who_args['mdproviders'] = []

    if form_identities:
        who_args['identifiers'].insert(0, ('main_identifier', form_plugin))
    who_args['authenticators'].append(authenticator)
    who_args['mdproviders'].append(metadata)
    who_args['identifiers'].append(identifier)
    who_args['challengers'].append(challenger)

    return setup_auth(app, group_adapters, perm_adapters, **who_args)

