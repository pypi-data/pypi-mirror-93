# django-mellon - SAML2 authentication for Django
# Copyright (C) 2014-2019 Entr'ouvert
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals
import logging

from django.contrib.auth.backends import ModelBackend

from . import utils

logger = logging.getLogger(__name__)


class SAMLBackend(ModelBackend):
    def authenticate(self, request=None, **credentials):
        saml_attributes = credentials.get('saml_attributes') or {}
        # without an issuer we can do nothing
        if 'issuer' not in saml_attributes:
            logger.debug('no idp in saml_attributes')
            return None
        idp = utils.get_idp(saml_attributes['issuer'])
        if not idp:
            logger.debug('unknown idp %s', saml_attributes['issuer'])
            return None
        adapters = utils.get_adapters(idp, request=request)
        for adapter in adapters:
            if not hasattr(adapter, 'authorize'):
                continue
            if not adapter.authorize(idp, saml_attributes):
                return
        for adapter in adapters:
            if not hasattr(adapter, 'lookup_user'):
                continue
            user = adapter.lookup_user(idp, saml_attributes)
            if user:
                break
        else:  # no user found
            return
        for adapter in adapters:
            if not hasattr(adapter, 'provision'):
                continue
            adapter.provision(user, idp, saml_attributes)
        return user
