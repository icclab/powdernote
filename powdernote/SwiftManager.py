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

import collections
import re
from distutils import util
from swiftclient.client import put_object, get_container, get_object, delete_object, post_object
from Configuration import Configuration
from Note import Note
from MetaManager import MetaManager
from OutputManager import OutputManager
from VersionManager import VersionManager

class SwiftManager(object):

    IDREGEX = "^([0-9]+)\s-\s"
    TITLEREGEX = IDREGEX + "(.*)"
    IDSEP = " - "
    CRDATEIMP = "Date of creation: "
    LASTMODIMP = ", \nLast modified: "
    TAGSIMP = ", \nTags: "
    METAIMP = "\n---\n"

    '''
    objid = id - title
    1. objid -> id
    2. objid -> title
    3. given id and object id return title if objid matches, else None

    Replace uses of regex with calls to static methods
    SwiftManager.methodName()
    '''

    def __init__(self, storage_url, token):
        super(SwiftManager, self).__init__()
        self._storage_url = storage_url
        self._token = token
        self._downloadedNotesList = {}

    @staticmethod
    def objIdToId(objId):
        '''
        From an objectid of the form "1 - forest", returns only the id, e.g. 1
        as a string

        :param objId: The object id from which to get the id
        :return: A string representing the id
        '''
        match = re.match(SwiftManager.IDREGEX, objId)
        if match is not None:
            return match.group(1)
        else:
            return None

    @staticmethod
    def objIdToTitle(objId):
        '''
        Example: 1 - a --> a
        '''
        match = re.match(SwiftManager.TITLEREGEX, objId)
        if match is not None:
            return match.group(2)
        else:
            return None


    def getNote(self, noteId):
        objectIds = self.downloadObjectIds()
        for objectId in objectIds:
            if str(noteId) == SwiftManager.objIdToId(objectId):
                noteContent = self._downloadNote(objectId)
                note = Note(SwiftManager.objIdToTitle(objectId))
                note.setObjectId(objectId)
                note.setContent(noteContent)
                return note
        return None

    def uploadNote(self, note, title):
        if len(title) == 0:
            title = self._generateObjectTitle(note.getTitle())
        metaManager = MetaManager(self._storage_url, self._token, title)
        currentCreateDate = metaManager.getCreateDate()
        put_object(self._storage_url, self._token, Configuration.container_name, title,
                   note.getContent().encode('utf-8'))
        lastModifiedDate = MetaManager.dateNow()
        # currentCreateDate may be None because note may be new
        # this comment is just a companion for the one above, he felt lonely
        if currentCreateDate is None:
            currentCreateDate = lastModifiedDate

        metaManager.setCreateDate(currentCreateDate)
        metaManager.setLastModifiedDate(lastModifiedDate)
        # we only need to keep the previous tags, NONE IS CORRECT DO NOT CHANGE
        metaManager.setTags(None)
        metaManager.commitMeta()
        print title
        return title

    def _renameNote(self, newTitle, oldTitle):
        put_object(self._storage_url, self._token, Configuration.container_name, newTitle, headers={"X-Copy-From":Configuration.container_name + "/" + oldTitle})
        self._deleteNoteByObjectId(oldTitle)


        metaManager = MetaManager(self._storage_url, self._token, newTitle)
        currentCreateDate = metaManager.getCreateDate()
        lastModifiedDate = MetaManager.dateNow()

        metaManager.setCreateDate(currentCreateDate)
        metaManager.setLastModifiedDate(lastModifiedDate)
        metaManager.setTags(None)
        metaManager.commitMeta()

        print "Ok"

    def versionUpload(self, oldTitle, newTitle):
        '''
        uploads a version
        :param oldTitle:
        :param newTitle:
        :return:
        '''
        put_object(self._storage_url, self._token, Configuration.container_name, newTitle, headers={"X-Copy-From":Configuration.container_name + "/" + oldTitle})


    def deleteNote(self, id, force = False):
        _, objects = self._downloadContainer()
        for object in objects:
            if str(id) == SwiftManager.objIdToId(object['name']):
                if force or self.confirmation("delete note \'" + object['name'] + "\'"):
                    self._deleteNoteByObjectId(object['name'])
                    if force == False:
                        print "Ok"
                else:
                    print "Abort"
                return

    def _deleteNoteByObjectId(self, objectId):
        delete_object(self._storage_url, self._token, Configuration.container_name, objectId)

    def downloadObjectIds(self):
        containerInfo, objects = self._downloadContainer()
        titles = []
        for object in objects:
            titles.append(object['name'])
        return titles

    def downloadNotes(self):
        notetitles = self.downloadObjectIds()
        for noteName in notetitles:
            noteContent = self._downloadNote(noteName)
            self._downloadedNotesList[noteName] = noteContent

        self._downloadedNotesList = collections.OrderedDict(sorted(self._downloadedNotesList.items()))

    def getDownloadedNotes(self):
        return self._downloadedNotesList

    def _generateObjectId(self):
        _, objects = self._downloadContainer()

        objectsIds = []

        for object in objects:
            objectName = object['name']
            try:
                id = re.match(self.IDREGEX, objectName).group(1)
            except AttributeError:
                continue
            objectsIds.append(int(id))
        objectsIds.sort()

        left = 0
        id = 0

        for id in objectsIds:
            if id - left > 1:
                return str (left + 1)
            left = id
        return (id + 1)

    def _generateObjectTitle(self, title):
        id = self._generateObjectId()
        objectTitleId = str(id) + self.IDSEP + title
        return objectTitleId

    def _downloadNote(self, noteId):
        return get_object(self._storage_url, self._token, Configuration.container_name, noteId)[1]

    def _downloadContainer(self):
        return get_container(self._storage_url, self._token, Configuration.container_name)

    def confirmation(self, action):
        '''
        asks for confirmation of an action
        :param action:
        :return:
        '''
        confirm = None
        while confirm == None:
            try:
                answer = raw_input("Are you sure you want to " + action + "? (y/n) ")
                confirm = util.strtobool(answer)
            except ValueError:
                print "Try again"
                continue

        if confirm == 1:
            return True
        else:
            return False

    def printMeta(self, metaId):
        '''
        prints the metadata of a single note
        :param metaId:
        :return:
        '''
        dict = {}
        note = self.getNote(metaId)
        mm = self.metaManagerFactory(note.getObjectId())
        name = SwiftManager.objIdToTitle(note.getObjectId())
        crDate = mm.getCreateDate()
        lastmod = mm.getLastModifiedDate()
        tags = mm.getTags()
        dict[metaId] = [metaId, name, crDate, lastmod, tags]
        sorted(dict)

        OutputManager.listPrint(dict, OutputManager.HEADER_FULL)

    def metaManagerFactory(self, objId):
        # vince said factories are self explanatory, no need to further comment
        # I still don' really know what a factory does
        return MetaManager(self._storage_url, self._token, objId)

    def addTags(self, tags, tId):
        '''
        saves tags to the metadata of note, and then commits it to swift
        :param tags:
        :param tId:
        :return:
        '''
        note = self.getNote(tId)
        mm = self.metaManagerFactory(note.getObjectId())
        mm.loadData()
        mm.setTags(tags)
        mm.commitMeta()

    def doesNoteExist(self, id):
        list = self.downloadObjectIds()
        idList = []
        for element in list:
            if VersionManager.isAnoteVersion(element) or VersionManager.isAnoteDeleted(element):
                continue
            oId = SwiftManager.objIdToId(element)
            idList.append(int(oId))
        if id not in idList:
            return False
        else:
            return True

    def rawupload(self, objectid, content, metadict):
        put_object(self._storage_url, self._token, Configuration.container_name, objectid,
                   content.encode('utf-8'))
        mm = self.metaManagerFactory(objectid)
        mm.setRawMetaDictionary(metadict)
        mm.commitMeta()