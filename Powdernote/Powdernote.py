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

import sys
from tabulate import tabulate
from EditorManager import EditorManager
from SwiftManager import SwiftManager
from SwiftAuthManager import SwiftAuthManager
from Note import Note

class Powdernote(object):

    NOTE_INDICATOR = " \n --- \n"
    NOTE = "Note: \n "
    TAGS = "\nCoresponding tags: \n "

    def __init__(self):
        super(Powdernote, self).__init__()
        self._editorManager = EditorManager()
        sam = SwiftAuthManager()
        storage_url, token = sam.getcredentials()
        self._swiftManager = SwiftManager(storage_url, token)

    def newNote(self, title):
        note = Note(title)
        self._editNote(note)

    def editNote(self, id):
        note = self._swiftManager.getNote(id)
        self._editNote(note)

    def readNote(self, id):
        note = self._swiftManager.getNote(id)
        self._readNote(note)

    def listNote(self):
        list = self._swiftManager.downloadObjectIds()
        dict = {}
        for element in list:
            id = SwiftManager.objIdToId(element)
            if id is None:
                continue
            id = int(id)
            dict[id] = element
            sorted(dict)

        for key, values in dict.items():
            print values

    def listNotesAndMeta(self):
        list = self._swiftManager.downloadObjectIds()
        dict  = {}
        table = []
        for element in list:
            id = SwiftManager.objIdToId(element)
            if id is None:
                raise RuntimeError("Can not get the ID from " + element + " ... should not happen, really")
            metamngr = self._swiftManager.metaMngrFactory(element)
            id = int(id)
            crdate = metamngr.getCreateDate()
            lastmod = metamngr.getLastModifiedDate()
            tags = metamngr.getTags()
            dict[id] = [element, crdate, lastmod, tags]
            sorted(dict)

        for key, value in dict.items():
            table.append(value)
        print tabulate(table, headers=["Note", "Creation Date", "Last Modified", "Tags"])

    def deleteNote(self, id):
        self._swiftManager.deleteNote(id)

    def _editNote(self, note):
        # TODO: validate note content (even if existing content coming from online should always be valid if only edited with this application)
        # raise exception if note content was not valid
        
        # TODO: edit note in a loop until the content is valid
        ret = self._editorManager.editNote(note)
        if ret == EditorManager.NEW_CONTENT_AVAILABLE:
            self._swiftManager.uploadNote(note)
            print "note has been saved"
        else:
            print "no changes have been made, aborting..."
            sys.exit(1)

    def searchInTitle(self, subString):
        titles = self._swiftManager.downloadObjectIds()
        for title in titles:
            title = title.lower()
            subString = subString.lower()
            loc = title.find(subString)
            if loc < 0:
                continue
            else:
                print title

    def searchInMushroom(self, substr):
        self._swiftManager.downloadNotes()
        notes = self._swiftManager.getDownloadedNotes()
        for noteName, noteContent in notes.items():
            substr = substr.lower()
            noteContent = noteContent.lower()
            loc = noteContent.find(substr)
            if loc < 0:
                continue
            else:
                print noteName


    def searchInTags(self, substr):
        '''
        for every object in list check for tags
        check if tags are the same
        if tags in element meta
        print element name
        '''

        self._swiftManager.downloadNotes()
        notes = self._swiftManager.getDownloadedNotes()
        for noteName in notes:
            metamngr = self._swiftManager.metaMngrFactory(noteName)
            tags = metamngr.getTags()
            if tags == "" or tags is None:
                continue
            tagList = tags.lower().split()
            substr = substr.lower()
            if substr in tagList:
                print Powdernote.NOTE_INDICATOR + Powdernote.NOTE + noteName + Powdernote.TAGS + tags + Powdernote.NOTE_INDICATOR

    def _readNote(self, note):
        print Powdernote.NOTE_INDICATOR + note.getContent() + Powdernote.NOTE_INDICATOR

    def printMeta(self, metaId):
        self._swiftManager.printMeta(metaId)

    def addTags(self, tags, objId):
        self._swiftManager.addTags(tags, objId)