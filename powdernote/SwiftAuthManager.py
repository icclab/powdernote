# -*- coding: utf-8 -*-

'''
Copyright 2015 ZHAW (Zürcher Hochschule für Angewandte Wissenschaften)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

__author__ = 'gank'

from swiftclient.client import Connection
from Configuration import Configuration


class SwiftAuthManager(object):

    def __init__(self):
        super(SwiftAuthManager, self).__init__()
        self._cnt = self._auth()

    def _auth(self):
        cnt = Connection(
            authurl=Configuration.auth_url,
            user=Configuration.username,
            key=Configuration.password,
            tenant_name=Configuration.tenant_name,
            auth_version=2,
            insecure=False)
        return cnt

    def getcredentials(self):
        storage_url, token = self._cnt.get_auth()
        return storage_url, token
