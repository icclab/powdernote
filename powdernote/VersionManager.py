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

from OutputManager import OutputManager
from datetime import datetime

class VersionManager(object):

        VERSIONIDENTIFIER = "v"
        DELETEIDENTIFIER = "vd"
        ZEROPAD = ":00.000000"

        def __init__(self, swiftManager):
            super(VersionManager, self).__init__()
            self._swiftMngr = swiftManager

        def versionCreator(self, objectId):
            #todo: comments

            if objectId not in self._swiftMngr.downloadObjectIds():
                return

            metamngr = self._swiftMngr.metaMngrFactory(objectId)
            metaTime = metamngr.getLastModifiedDate(cutToSeconds=False)

            #support legacy notes
            if len(metaTime) == 17:
                metaTime = metaTime[:5] + VersionManager.ZEROPAD + metaTime[5:]

            time = datetime.strptime(metaTime, '%H:%M:%S.%f, %d/%m/%Y')
            versionTime = time.strftime("%Y%m%d%H%M%S%f")[:-3]

            oldTitle = objectId
            newTitle = VersionManager.VERSIONIDENTIFIER + OutputManager.DASH + versionTime + OutputManager.DASH \
                       + self._swiftMngr.objIdToId(oldTitle)
            self._swiftMngr.versionUpload(oldTitle, newTitle)


        @staticmethod
        def isAnoteVersion(objectId):
            '''
            checks if the object is a version
            :param objectId:
            :return:
            '''
            if objectId.startswith("v-"):
                return True
            return False

        @staticmethod
        def isAnoteDeleted(objectId):
            '''
            checks if the object is a deleted note
            :param objectId:
            :return:
            '''
            if objectId.startswith("vd-"):
                return True
            return False


        def historyList(self, noteId, allVersions, title):
            #todo: comments

            versionsOfNote = {}
            versionId = 0
            noteId = str(noteId)
            for element in allVersions:
                versionId = versionId + 1
                if noteId in element[20:len(element)]:
                    versionsOfNote[versionId] = [versionId, element, title]
                else:
                    continue

            return versionsOfNote

        def deleteVersionCreator(self, noteId, title):
            #todo: comments

            #the reason why the delete is in the beginning, is because the version that is being created in this
            #method would also be deleted if the method would be called in the end
            self.versionDelete(noteId)

            objectId = noteId + OutputManager.ID_TITLE_SEPERATOR + title
            versionType = VersionManager.DELETEIDENTIFIER

            self._versionUploader(objectId, versionType)

        def versionDelete(self, noteId):
            #todo: comments
            #delete the versions

        def _versionUploader(self, objectId, versionType):
            #todo: comments

            if objectId not in self._swiftMngr.downloadObjectIds():
                return

            metamngr = self._swiftMngr.metaMngrFactory(objectId)
            metaTime = metamngr.getLastModifiedDate(cutToSeconds=False)

            #support legacy notes
            if len(metaTime) == 17:
                metaTime = metaTime[:5] + VersionManager.ZEROPAD + metaTime[5:]

            time = datetime.strptime(metaTime, '%H:%M:%S.%f, %d/%m/%Y')
            versionTime = time.strftime("%Y%m%d%H%M%S%f")[:-3]

            oldTitle = objectId
            if versionType == VersionManager.VERSIONIDENTIFIER:
                identifier = VersionManager.VERSIONIDENTIFIER

            elif versionType == VersionManager.DELETEIDENTIFIER:
                identifier = VersionManager.DELETEIDENTIFIER

            newTitle = identifier + OutputManager.DASH + versionTime + OutputManager.DASH \
                       + self._swiftMngr.objIdToId(oldTitle)

            self._swiftMngr.versionUpload(oldTitle, newTitle)