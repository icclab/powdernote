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

from datetime import datetime
from swiftclient.client import post_object, get_object
from swiftclient.exceptions import ClientException
from Configuration import Configuration
from VersionManager import VersionManager
import re

class MetaManager(object):

    CRDATE_META_KEY = 'x-object-meta-crdate'
    LASTMOD_META_KEY = 'x-object-meta-lastmod'
    TAGS_META_KEY = 'x-object-meta-tags'

    def __init__(self, url, token, objectId):
        super(MetaManager, self).__init__()
        self._url = url
        self._token = token
        self._commitList = {}
        self._objId = objectId
        self._meta = None
        self.update()
        # self._commitList = self._meta

    @staticmethod
    def dateNow():
        nowDate = datetime.now()
        return nowDate.strftime('%H:%M:%S.%f, %d/%m/%Y')

    def loadData(self):
        self._commitList[MetaManager.CRDATE_META_KEY] = self._getMeta(MetaManager.CRDATE_META_KEY)
        self._commitList[MetaManager.LASTMOD_META_KEY] = self._getMeta(MetaManager.LASTMOD_META_KEY)
        self._commitList[MetaManager.TAGS_META_KEY] = self._getMeta(MetaManager.TAGS_META_KEY)

    def _cutTimestampStringToSeconds(self, timestamp):
        '''
        this function makes the microseconds invisible in the timestamp string of a note metadata when it's getting
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
        timestamp = self._getMeta(MetaManager.CRDATE_META_KEY)
        return self._getTimestampInformation(timestamp, cutToSeconds)

    def getLastModifiedDate(self, cutToSeconds=True):
        timestamp = self._getMeta(MetaManager.LASTMOD_META_KEY)
        return self._getTimestampInformation(timestamp, cutToSeconds)

    def _getTimestampInformation(self, timestamp, cutToSeconds):
        if not timestamp:
            return None
        # support legacy notes
        if MetaManager.isLegacyTimestamp(timestamp):
            timestamp = MetaManager.convertLegacyTimestamp(timestamp)
        if cutToSeconds:
            timestamp = self._cutTimestampStringToSeconds(timestamp)
        return timestamp

    def getTags(self):
        return self._getMeta(MetaManager.TAGS_META_KEY)

    def _getMeta(self, metaHeader):
        '''
        Given a metadata header name, returns its value.
        :param metaHeader: string of the metadata header, e.g., 'x-object-meta-lastmod'
        :return: None if no metadata is available for this object or the value is not available,
        the value for this metadata otherwise
        '''
        if self._meta == None:
            return None
        return self._meta.get(metaHeader)

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

    @staticmethod
    def isLegacyTimestamp(timestamp):
        '''
        Returns true if the given timestamp is a legacy one (before we introduced usec timestamps for versioning)
        '''
        return len(timestamp) == VersionManager.LEGACY_FORMAT_LENGTH

    @staticmethod
    def convertLegacyTimestamp(timestamp):
        '''
        Pads a legacy timestamp (e.g., 09:21, 03/12/2014) with zeros so its length is like a usec one (e.g.,
        '09:21:00.000000, 03/12/2014)
        '''
        timestamp = timestamp[:5] + VersionManager.ZEROPAD + timestamp[5:]
        return timestamp