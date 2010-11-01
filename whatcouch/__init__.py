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
This package provides group and permission adapters as well as authenticator
and metadata plugins.  Refer to the repoze.what documentation on how to use
them directly.

A quickstart method, setup_couch_auth, is included which simplifies the
process.  This is similar to the setup_sql_auth which is included in the
quickstart plugin.  A good bit of customization is available when using the
included quickstart method.  Combined with the provided example model you can
be up and running fairly quickly.

In order to use the example model you'll need to load the included views.
They can be found in the model.py file.
"""

from whatcouch.adapters import GroupAdapter, PermissionAdapter
from whatcouch.plugins import AuthenticatorPlugin, MetadataPlugin
from whatcouch.quickstart import setup_couch_auth

__all__ = ['GroupAdapter', 'PermissionAdapter', 'AuthenticatorPlugin', 'MetadataPlugin', 'setup_couch_auth']

