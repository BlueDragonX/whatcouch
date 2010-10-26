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
This module provides a quickstart function similar to that provided by the
repoze.what quickstart plugin.
"""

from repoze.who.plugins.auth_tkt import AuthTktCookiePlugin
from repoze.who.plugins.friendlyform import FriendlyFormPlugin
from repoze.what.middleware import setup_auth
from whatcouch.adapters import GroupAdapter, PermissionAdapter
from whatcouch.plugins import AuthenticatorPlugin, MetadataPlugin
from whatcouch.model import User, Group, Permission

"""
Default translations.  These will be substituted for missing values
in the translations dict that's passed to the quickstart function.
See wrappers.py for documentation on the translations dict.
"""
default_translations = {
    'user_name_key': 'username',
    'user_groups_key': 'groups',
    'user_find_by_name': 'find_by_username',
    'user_find_by_group': 'find_by_group_name',
    'user_authenticate': 'authenticate',
    'group_name_key': 'name',
    'group_perms_key': 'permissions',
    'group_list': 'list',
    'group_find_by_name': 'find_by_name',
    'group_find_by_perm': 'find_by_permission_name',
    'perm_name_key': 'name',
    'perm_list': 'list',
    'perm_find_by_name': 'find_by_name',
    'perm_find_by_group': 'find_by_group_name'}

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

