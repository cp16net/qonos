# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2011 OpenStack LLC.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""
A filter middleware that inspects the requested URI for a version string
and/or Accept headers and attempts to negotiate an API controller to
return
"""

from chronos.api import versions
from chronos.openstack.common import wsgi
import chronos.openstack.common.log as logging
from chronos.openstack.common import cfg
from chronos.openstack.common.gettextutils import _

CONF = cfg.CONF

LOG = logging.getLogger(__name__)


class VersionNegotiationFilter(wsgi.Middleware):

    def __init__(self, app):
        self.versions_app = versions.Controller()
        super(VersionNegotiationFilter, self).__init__(app)

    def process_request(self, req):
        """Try to find a version first in the accept header, then the URL"""
        msg = _("Determining version of request: %(method)s %(path)s"
                " Accept: %(accept)s")
        args = {'method': req.method, 'path': req.path, 'accept': req.accept}
        LOG.debug(msg % args)

        accept = str(req.accept)
        if accept.startswith('application/vnd.openstack.chronos-'):
            LOG.debug(_("Using media-type versioning"))
            token_loc = len('application/vnd.openstack.chronos-')
            req_version = accept[token_loc:]
        else:
            LOG.debug(_("Using url versioning"))
            # Remove version in url so it doesn't conflict later
            req_version = req.path_info_pop()
        try:
            version = self._match_version_string(req_version)
        except ValueError:
            LOG.debug(_("Unknown version. Returning version choices."))
            return self.versions_app

        req.environ['api.version'] = version
        req.path_info = ''.join(('/v', str(version), req.path_info))
        LOG.debug(_("Matched version: v%d"), version)
        LOG.debug('new uri %s' % req.path_info)
        return None

    def _match_version_string(self, subject):
        """
        Given a string, tries to match a major and/or
        minor version number.

        :param subject: The string to check
        :returns version found in the subject
        :raises ValueError if no acceptable version could be found
        """
        if subject in ('v1', 'v1.0'):
            major_version = 1
        else:
            raise ValueError()

        return major_version

    @classmethod
    def factory(cls, global_conf, **local_conf):
        def filter(app):
            return cls(app)
        return filter