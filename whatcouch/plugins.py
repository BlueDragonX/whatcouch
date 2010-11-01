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
This module contains repoze.who authenticator and metadata plugins.
See the repoze.who documentation at <> for additional details.
"""

from zope.interface import implements
from repoze.who.interfaces import IAuthenticator, IMetadataProvider

__all__ = ['AuthenticatorPlugin', 'MetadataPlugin']

class AuthenticatorPlugin:
    """
    CouchDB authenticator plugin.
    """
    implements(IAuthenticator)

    def __init__(self, translations):
        """
        Constructor.  Configures the plugin with the given translations dict.
        :param translations: The translations to use when mapping requests against a model.
        """
        self.t11 = translations
        self.User = self.t11['user_class']
        self.user_name_key = self.t11['user_name_key']
        self.user_list_view = self.t11['user_list_view']
        self.user_auth_method = self.t11['user_auth_method']

    def authenticate(self, environ, identity):
        """
        Authenticate an identity against a CouchDB User document.
        :param environ: WSGI environment.
        :param identity: Identity dict for the user.
        """
        if 'login' in identity and 'password' in identity:
            users = self.User.view(self.user_list_view, key=identity['login'])
            if len(users) > 0:
                user = users.__iter__().next()
                auth = getattr(user, self.user_auth_method)
                if auth(identity['password']):
                    return getattr(user, self.user_name_key)
        return None

class MetadataPlugin:
    implements(IMetadataProvider)

    def __init__(self, translations):
        """
        Constructor.  Configures the plugin with the given translations dict.
        :param translations: The translations to use when mapping requests against a model.
        """
        self.t11 = translations
        self.User = self.t11['user_class']
        self.user_list_view = self.t11['user_list_view']

    def add_metadata(self, environ, identity):
        """
        Add metadata to an identity dict from the associated CouchDB User document.
        :param environ: WSGI environment.
        :param identity: Identity dict for the user.
        """
        if 'repoze.who.userid' in identity:
            users = self.User.view(self.user_list_view, key=identity['repoze.who.userid'])
            if len(users) > 0:
                identity['user'] = users.__iter__().next()

