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

from swiftclient.client import put_object, get_container, get_object, delete_object
from Configuration import Configuration
import collections
import re
from distutils import util
from Note import Note

class SwiftManager(object):

    IDREGEX = "^([0-9]+)\s-\s"
    TITLEREGEX = IDREGEX + "(.*)"
    IDSEP = " - "

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

    def uploadNote(self, note):
        title = self._generateObjectTitle(note.getTitle())
        put_object(self._storage_url, self._token, Configuration.container_name, title,
                   note.getContent())

    def deleteNote(self, id):
        _, objects = self._downloadContainer()
        for object in objects:
            if str(id) == SwiftManager.objIdToId(object['name']):
                if self._confirmation("delete note \'" + object['name'] + "\'"):
                    self._deleteNoteByObjectId(object['name'])
                    print "note deleted"
                else:
                    print "abort"
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

    def _confirmation(self, action):
        confirm = None
        while confirm == None:
            try:
                answer = raw_input("are you sure you want to " + action + "? (y/n) ")
                confirm = util.strtobool(answer)
            except ValueError:
                print "try again"
                continue

        if confirm == 1:
            return True
        else:
            return False