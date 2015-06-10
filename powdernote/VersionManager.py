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

from OutputManager import OutputManager
from datetime import datetime
import re
from collections import defaultdict

class VersionManager(object):

    VERSIONIDENTIFIER = "v"
    DELETEIDENTIFIER = "vd"
    DELETEID = "d"
    ZEROPAD = ":00.000000"

    LEGACY_FORMAT_SAMPLE = "09:21, 03/12/2014"
    LEGACY_FORMAT_LENGTH = len(LEGACY_FORMAT_SAMPLE)

    VERSION_ID_REGEX = "^(v-\d+-)(\d+)"

    def __init__(self, swiftManager):
        super(VersionManager, self).__init__()
        self._swiftMngr = swiftManager

    def _downloadAllNoteVersions(self):
        '''
        extracts all the objects that start with "v" and appends them to a list
        :return:
        '''
        versions = []
        listOfAllObjects = self._swiftMngr.downloadObjectIds()
        for element in listOfAllObjects:
            if self.isAnoteVersion(element):
                versions.append(element)
            else:
                continue
        return versions

    def _downloadAllDeleted(self):
        '''
        extracts all the objects that start with "vd" and appends them to a list
        :return:
        '''
        deleted = []
        listOfAllObjects = self._swiftMngr.downloadObjectIds()
        for element in listOfAllObjects:
            if self.isAnoteDeleted(element):
                deleted.append(element)
            else:
                continue
        return deleted

    @staticmethod
    def extractId(objectId):
        '''
        extracts and returns the id of a version, e.g.: v-20150511101307105-15 --> 15
        :param objectId:
        :return:
        '''
        regex = VersionManager.VERSION_ID_REGEX
        return re.search(regex, objectId).group(2)

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

    @staticmethod
    def isVersionOrDeleted(objectId):
        '''
        Only backup of deleted notes or note versions can start with v
        '''
        if objectId.startswith("v"):
            return True
        return False

    @staticmethod
    def changeId(objectId, newid):
        '''

        :param objectId: the full object id (e.g., v-20150521151505633-17)
        :param newid: the new id (e.g., 18)
        :return: the full object id with the new id, e.g. v-20150521151505633-18
        '''
        regex = VersionManager.VERSION_ID_REGEX
        return re.match(regex, objectId).group(1) + newid


    def historyList(self, noteId, allVersions, title):
        '''
        creates a list of the versions of the given note
        :param noteId:
        :param allVersions:
        :param title:
        :return:
        '''

        versionsOfNote = {}
        versionId = 0
        for version in allVersions[str(noteId)]:
            versionId = versionId + 1
            # add the versions to the dict
            versionsOfNote[versionId] = [versionId, version, title]
        return versionsOfNote

    def deleteVersionCreator(self, noteId, title):
        '''
        deletes the versions of a note and also creates the back up
        :param noteId:
        :param title:
        :return:
        '''
        objectId = noteId + OutputManager.ID_TITLE_SEPERATOR + title
        versionType = VersionManager.DELETEIDENTIFIER

        # upload the back up
        self._versionUploader(objectId, versionType)
        # delete all the versions of the note
        self.versionDelete(noteId)

    def versionDelete(self, noteId):
        '''
        deletes the versions of a note that is about to be deleted
        :param noteId:
        :return:
        '''
        note, title, versions, noteList = self._getVersionInfo(noteId, output=False)
        for _, value in versions.iteritems():
            # delete a note by ObjectId
            self._swiftMngr._deleteNoteByObjectId(value[1])

    def _versionUploader(self, objectId, versionType):
        '''
        uploads a version or a backup of a note
        :param objectId:
        :param versionType:
        :return:
        '''
        if objectId not in self._swiftMngr.downloadObjectIds():
            return

        # get the timestamps
        metamngr = self._swiftMngr.metaManagerFactory(objectId)
        metaTime = metamngr.getLastModifiedDate(cutToSeconds=False)

        # support legacy notes
        if len(metaTime) == 17:
            # legacy notes don't have seconds or microseconds, here they are added
            metaTime = metaTime[:5] + VersionManager.ZEROPAD + metaTime[5:]

        # transform the timestamp, to the right format
        time = datetime.strptime(metaTime, '%H:%M:%S.%f, %d/%m/%Y')
        versionTime = time.strftime("%Y%m%d%H%M%S%f")[:-3]

        # get only the title
        title = self._swiftMngr.objIdToTitle(objectId)
        oldTitle = objectId
        if versionType == VersionManager.VERSIONIDENTIFIER:
            # compose the new title if it is a version, so with the "v-"
            newTitle = VersionManager.VERSIONIDENTIFIER + OutputManager.DASH + versionTime + OutputManager.DASH \
                   + self._swiftMngr.objIdToId(oldTitle)

        elif versionType == VersionManager.DELETEIDENTIFIER:
            # compose new title if it is a back up, so with the "vd-"
            newTitle = VersionManager.DELETEIDENTIFIER + OutputManager.DASH + versionTime + OutputManager.DASH \
                   + VersionManager.DELETEID + OutputManager.ID_TITLE_SEPERATOR + title

        self._swiftMngr.versionUpload(oldTitle, newTitle)

    def _getVersionInfo(self, noteId, output=True):
        '''
        prints and returns a list of the versions of the given note
        :param noteId:
        :param output:
        :return:
        '''
        # a list with a list of objects that start with "v"
        allVersions = self._downloadAllNoteVersions()

        self._swiftMngr.downloadNotes()
        # a list with the content for each object
        noteList = self._swiftMngr.getDownloadedNotes()

        note = self._swiftMngr.getNote(noteId)
        title = note.getTitle()
        # a list of all the versions with a continuos Id
        versions = self.historyList(noteId, self.arrangeNoteVersions(allVersions), title)
        # rearanges the ids so each note's versions start counting from 1
        # rearangedVersions = self.rearangeVersionID(versions)

        if output == True:
            # nicely prints the versions list
            OutputManager.listPrint(versions, 3)

        return note, title, versions, noteList

    def getDeletedInfo(self, output = True):
        '''
        prints and returns a list of backed up notes
        :param output:
        :return:
        '''
        allDeleted= self._downloadAllDeleted()

        deletedList = {}
        deletedId = 0

        for element in allDeleted:
            # assign an id to all objects and save it in a dict
            deletedId = deletedId + 1
            deletedList[deletedId] = [deletedId, element]

        if output == True:
            # nicely prints the backed up notes list
            OutputManager.listPrint(deletedList, 4)

        return deletedList

    def arrangeNoteVersions(self, allVersions):
        '''
        produces a dict that for each id creates a list of versions
        :param allVersions:
        :return:
        '''
        versions = defaultdict(list)
        for element in allVersions:
            noteId = VersionManager.extractId(element)
            versions[noteId].append(element)
        return versions