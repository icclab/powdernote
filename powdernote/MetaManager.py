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
import re

class MetaManager(object):

    def __init__(self, url, token, objectId):
        super(MetaManager, self).__init__()
        self._url = url
        self._token = token
        self._commitList = {}
        self._objId = objectId
        self._meta = None
        self.update()
        #self._commitList = self._meta

    @staticmethod
    def dateNow():
        nowDate = datetime.now()
        return nowDate.strftime('%H:%M:%S.%f, %d/%m/%Y')

    def loadData(self):
        self._commitList['x-object-meta-crdate'] = self._getMeta('x-object-meta-crdate')
        self._commitList['x-object-meta-lastmod'] = self._getMeta('x-object-meta-lastmod')
        self._commitList['x-object-meta-tags'] = self._getMeta('x-object-meta-tags')

    def _cutTimestampStringToSeconds(self, timestamp):
        '''
        this function makes the microseconds invisible in the timestamp string of a notes metadata when it's getting
        listed, so there is not too much information that it looks confusing.
        :param timestamp:
        :return:
        '''
        regex = '^(\d+:\d+:\d+)\.\d+(,.*)$'
        cut = re.search(regex, timestamp)
        # support legacy notes that do not have the new timestamp
        if cut is None:
            return timestamp
        cutSeconds = cut.group(1)+cut.group(2)
        return cutSeconds

    def getCreateDate(self, cutToSeconds=True):
        # use _getMeta
        #"other solution is very easy" ~ Vincenzo Pii, 2014 Zürich
        timestamp = self._getMeta('x-object-meta-crdate')
        if cutToSeconds:
            return self._cutTimestampStringToSeconds(timestamp)
        else:
            return timestamp

    def getLastModifiedDate(self, cutToSeconds=True):
        timestamp = self._getMeta('x-object-meta-lastmod')
        if cutToSeconds:
            return self._cutTimestampStringToSeconds(timestamp)
        else:
            return timestamp


    def getTags(self):
        return self._getMeta('x-object-meta-tags')

    def _getMeta(self, metaHeader):
        '''
        Given a metadata header name, returns its value.
        :param metaHeader: string of the metadata header, e.g., 'x-object-meta-lastmod'
        :return: None if no metadata is available for this object or the value is not available,
        the value for this metadata otherwise
        '''
        # Implement this
        if self._meta == None:
            return None
        if metaHeader in self._meta:
            return self._meta[metaHeader]
        else:
            return None

    def update(self):
        '''
        Updates the metadata information for this object
        :return:
        '''
        try:
            self._meta = get_object(self._url, self._token, Configuration.container_name, self._objId)[0]
        except ClientException:
            self._meta = None

    def setCreateDate(self, currentCreateDate):
        self._commitList['x-object-meta-crdate'] = currentCreateDate

    def setLastModifiedDate(self, lastModifiedDate):
        self._commitList['x-object-meta-lastmod'] = lastModifiedDate

    def setTags(self, tags):
        '''
        this function takes the users input as a list of tags
        :param tags: list expected
        :return:
        '''
        oldL = self._getMeta('x-object-meta-tags')
        if oldL is None:
            oldL = []
        else:
            oldL = oldL.split()
        if tags is None:
            tags = []
        oldL = oldL + tags
        oldL = set(oldL)
        oldL = ' '.join(oldL)
        self._commitList['x-object-meta-tags'] = oldL

    def commitMeta(self):
        if self._commitList != {}:
            post_object(self._url, self._token, Configuration.container_name, self._objId, self._commitList)
        self._commitList = {}