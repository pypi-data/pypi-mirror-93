# Copyright 2020 Red Hat, inc
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


import requests
import urllib.parse


class ZuulRESTException(Exception):
    pass


class BearerAuth(requests.auth.AuthBase):
    """Custom authentication helper class.

    Authentication helper class to work around requests' default behavior
    of using ~/.netrc to authenticate despite having set an explicit
    authorization header.
    See also https://github.com/psf/requests/issues/3929
    """

    def __init__(self, token):
        self._token = token

    def __call__(self, r):
        r.headers["Authorization"] = 'Bearer %s' % self._token
        return r


class ZuulRESTClient(object):
    """Basic client for Zuul's REST API"""
    def __init__(self, url, verify=False, auth_token=None):
        self.url = url
        if not self.url.endswith('/'):
            self.url += '/'
        self.auth_token = auth_token
        self.verify = verify
        self.base_url = urllib.parse.urljoin(self.url, 'api/')
        self.session = requests.Session()
        self.session.verify = self.verify
        if self.auth_token:
            self.session.auth = BearerAuth(self.auth_token)
        self.info_ = None

    @property
    def info(self):
        """Return the Zuul info data.
        Useful to get capabilities and tenant info."""
        if self.info_ is None:
            url = urllib.parse.urljoin(
                self.base_url,
                'info')
            req = self.session.get(url)
            self._check_request_status(req)
            self.info_ = req.json()
        return self.info_

    def _check_request_status(self, req):
        try:
            req.raise_for_status()
        except Exception as e:
            if req.status_code == 401:
                raise ZuulRESTException(
                    'Unauthorized - your token might be invalid or expired.')
            elif req.status_code == 403:
                raise ZuulRESTException(
                    'Insufficient privileges to perform the action.')
            else:
                raise ZuulRESTException(
                    'Unknown error code %s: "%s"' % (req.status_code, e))

    def autohold(self, tenant, project, job, change, ref,
                 reason, count, node_hold_expiration):
        if not self.auth_token:
            raise Exception('Auth Token required')
        args = {"reason": reason,
                "count": count,
                "job": job,
                "change": change,
                "ref": ref,
                "node_hold_expiration": node_hold_expiration}
        if self.info.get('tenant'):
            suffix = 'project/%s/autohold' % project
        else:
            suffix = 'tenant/%s/project/%s/autohold' % (tenant, project)
        url = urllib.parse.urljoin(
            self.base_url,
            suffix)
        req = self.session.post(url, json=args)
        self._check_request_status(req)
        return req.json()

    def autohold_list(self, tenant):
        if self.info.get('tenant'):
            suffix = 'autohold'
        else:
            suffix = 'tenant/%s/autohold' % tenant
        url = urllib.parse.urljoin(
            self.base_url,
            suffix)
        # auth not needed here
        req = self.session.get(url)
        self._check_request_status(req)
        resp = req.json()
        return resp

    def autohold_delete(self, id, tenant):
        if not self.auth_token:
            raise Exception('Auth Token required')
        if self.info.get('tenant'):
            suffix = 'autohold/%s' % id
        else:
            suffix = 'tenant/%s/autohold/%s' % (tenant, id)
        url = urllib.parse.urljoin(
            self.base_url,
            suffix)
        req = self.session.delete(url)
        self._check_request_status(req)
        # DELETE doesn't return a body, just the HTTP code
        return (req.status_code == 204)

    def autohold_info(self, id, tenant):
        if self.info.get('tenant'):
            suffix = 'autohold/%s' % id
        else:
            suffix = 'tenant/%s/autohold/%s' % (tenant, id)
        url = urllib.parse.urljoin(
            self.base_url,
            suffix)
        # auth not needed here
        req = self.session.get(url)
        self._check_request_status(req)
        resp = req.json()
        return resp

    def enqueue(self, tenant, pipeline, project, change):
        if not self.auth_token:
            raise Exception('Auth Token required')
        args = {"change": change,
                "pipeline": pipeline}
        if self.info.get('tenant'):
            suffix = 'project/%s/enqueue' % project
        else:
            suffix = 'tenant/%s/project/%s/enqueue' % (tenant, project)
        url = urllib.parse.urljoin(
            self.base_url,
            suffix)
        req = self.session.post(url, json=args)
        self._check_request_status(req)
        return req.json()

    def enqueue_ref(self, tenant, pipeline, project, ref, oldrev, newrev):
        if not self.auth_token:
            raise Exception('Auth Token required')
        args = {"ref": ref,
                "oldrev": oldrev,
                "newrev": newrev,
                "pipeline": pipeline}
        if self.info.get('tenant'):
            suffix = 'project/%s/enqueue' % project
        else:
            suffix = 'tenant/%s/project/%s/enqueue' % (tenant, project)
        url = urllib.parse.urljoin(
            self.base_url,
            suffix)
        req = self.session.post(url, json=args)
        self._check_request_status(req)
        return req.json()

    def dequeue(self, tenant, pipeline, project, change=None, ref=None):
        if not self.auth_token:
            raise Exception('Auth Token required')
        args = {"pipeline": pipeline}
        if change and not ref:
            args['change'] = change
        elif ref and not change:
            args['ref'] = ref
        else:
            raise Exception('need change OR ref')
        if self.info.get('tenant'):
            suffix = 'project/%s/dequeue' % project
        else:
            suffix = 'tenant/%s/project/%s/dequeue' % (tenant, project)
        url = urllib.parse.urljoin(
            self.base_url,
            suffix)
        req = self.session.post(url, json=args)
        self._check_request_status(req)
        return req.json()

    def promote(self, tenant, pipeline, change_ids):
        if not self.auth_token:
            raise Exception('Auth Token required')
        args = {'pipeline': pipeline,
                'changes': change_ids}
        if self.info.get('tenant'):
            suffix = 'promote'
        else:
            suffix = 'tenant/%s/promote' % tenant
        url = urllib.parse.urljoin(
            self.base_url,
            suffix)
        req = self.session.post(url, json=args)
        self._check_request_status(req)
        return req.json()

    def get_key(self, tenant, project):
        if self.info.get('tenant'):
            suffix = 'key/%s.pub' % project
        else:
            suffix = 'tenant/%s/key/%s.pub' % (tenant, project)
        url = urllib.parse.urljoin(
            self.base_url,
            suffix)
        req = self.session.get(url)
        self._check_request_status(req)
        return req.text
