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
        DELETEID = "d"
        ZEROPAD = ":00.000000"

        def __init__(self, swiftManager):
            super(VersionManager, self).__init__()
            self._swiftMngr = swiftManager
            self._versionList = []
            self._deletedNotes = []


        def downloadAllNoteVersions(self):
        #todo: comments
            listOfAllObjects = self._swiftMngr.downloadObjectIds()
            for element in listOfAllObjects:
                if self.isAnoteVersion(element):
                    self._versionList.append(element)
                else:
                    continue

        def downloadAllDeleted(self):
        #todo: comments
            listOfAllObjects = self._swiftMngr.downloadObjectIds()
            for element in listOfAllObjects:
                if self.isAnoteDeleted(element):
                    self._deletedNotes.append(element)
                else:
                    continue

        def getAllVersions(self):
            return self._versionList

        def getDeleted(self):
            return self._deletedNotes

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
            self.versionDelete(noteId)

        def versionDelete(self, noteId):
            #todo: comments
            '''
            deletes the versions of a note that is about to be deleted
            :param noteId:
            :return:
            '''
            note, title, versions, rearanged, noteList = self._getVersionInfo(noteId, output=False)
            for _, value in versions.iteritems():
                self._swiftMngr._deleteNoteByObjectId(value[1])


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

            title = self._swiftMngr.objIdToTitle(objectId)
            oldTitle = objectId
            if versionType == VersionManager.VERSIONIDENTIFIER:
                newTitle = VersionManager.VERSIONIDENTIFIER + OutputManager.DASH + versionTime + OutputManager.DASH \
                       + self._swiftMngr.objIdToId(oldTitle)

            elif versionType == VersionManager.DELETEIDENTIFIER:
                newTitle = VersionManager.DELETEIDENTIFIER + OutputManager.DASH + versionTime + OutputManager.DASH \
                       + VersionManager.DELETEID + OutputManager.ID_TITLE_SEPERATOR + title

            self._swiftMngr.versionUpload(oldTitle, newTitle)


        def _getVersionInfo(self, noteId, output=True):
            #todo: comments
            self.downloadAllNoteVersions()
            allVersions = self.getAllVersions()

            self._swiftMngr.downloadNotes()
            noteList = self._swiftMngr.getDownloadedNotes()

            note = self._swiftMngr.getNote(noteId)
            title = note.getTitle()
            versions = self.historyList(noteId, allVersions, title)

            rearangedVersions = self.rearangeVersionID(versions)

            if output == True:
                OutputManager.listPrint(rearangedVersions, 3)

            return note, title, versions, rearangedVersions, noteList

        def getDeletedInfo(self, output = True):
            self.downloadAllDeleted()
            allDeleted = self.getDeleted()

            deletedList = {}
            deletedId = 0

            for element in allDeleted:
                deletedId = deletedId + 1
                deletedList[deletedId] = [deletedId, element]

            if output == True:
                OutputManager.listPrint(deletedList, 4)

            return deletedList

        def rearangeVersionID(self, versions):
            #todo: comments

            newVersions = {}
            newVersionId = 0
            for key, value in versions.iteritems():
                noteTitle = versions[key][2]
                newVersionId = newVersionId + 1
                versionTitle = versions[key][1]
                newVersions[newVersionId] = [newVersionId, versionTitle, noteTitle]

            return newVersions