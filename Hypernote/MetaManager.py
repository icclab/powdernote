# -*- coding: utf-8 -*-

'''
Copyright 2014 ZHAW (Zürcher Hochschule für Angewandte Wissenschaften)

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

from datetime import datetime
from swiftclient.client import post_object, get_object
from swiftclient.exceptions import ClientException
from Configuration import Configuration


class MetaManager(object):

    def __init__(self, url, token, objectId):
        super(MetaManager, self).__init__()
        self._url = url
        self._token = token
        self._commitList = {}
        self._objId = objectId

    @staticmethod
    def dateNow():
        nowDate = datetime.now()
        return nowDate.strftime('%H:%M, %d/%m/%Y')


    def getCreateDate(self):
        try:
            meta = get_object(self._url, self._token, Configuration.container_name, self._objId)[0]
        except ClientException:
            return None
        crDate = meta['x-object-meta-crdate']
        return crDate

    def getLastModifiedDate(self):
        meta = get_object(self._url, self._token, Configuration.container_name, self._objId)[0]
        lastModifiedDate = meta['x-object-meta-lastmod']
        return lastModifiedDate

    def setCreateDate(self, currentCreateDate):
        self._commitList['x-object-meta-crdate'] = currentCreateDate

    def setLastModifiedDate(self, lastModifiedDate):
        self._commitList['x-object-meta-lastmod'] = lastModifiedDate

    def commitMeta(self):
        if self._commitList != {}:
            post_object(self._url, self._token, Configuration.container_name, self._objId, self._commitList)
        self._commitList = {}
