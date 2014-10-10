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
from EditorManager import EditorManager
from SwiftManager import SwiftManager
from SwiftAuthManager import SwiftAuthManager
from Note import Note

class NeverNote(object):

    def __init__(self):
        super(NeverNote, self).__init__()
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

    def listNote(self):
        list = self._swiftManager.downloadObjectIds()
        list.sort()
        for title in list:
            print title

    def deleteNote(self, id):
        self._swiftManager.deleteNote(id)

    def _editNote(self, note):
        ret = self._editorManager.editNote(note)
        if ret == EditorManager.NEW_CONTENT_AVAILABLE:
            self._swiftManager.uploadNote(note)
            print "note has been saved"
            # TODO: now delete the previous note
            print note.getObjectId()
            self._swiftManager.deleteNote(note.getObjectId())

        else:
            print "no changes have been made, aborting..."
            sys.exit(1)
