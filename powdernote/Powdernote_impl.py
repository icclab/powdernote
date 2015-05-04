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
from os.path import expanduser
from EditorManager import EditorManager
from SwiftManager import SwiftManager
from SwiftAuthManager import SwiftAuthManager
from Note import Note
from OutputManager import OutputManager
from ConfigParser import ConfigParser
from datetime import datetime
from collections import OrderedDict


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
        self._path = expanduser("~")


    def newNote(self, title):
        note = Note(title)
        self._editNote(note)

    def editNote(self, id):
        if self._swiftManager.doesNoteExist(id) == True:
            note = self._swiftManager.getNote(id)
            self._editNote(note)
        else:
            print "Note #" + str(id) + " doesn't exist"

    def readNote(self, id):
        if self._swiftManager.doesNoteExist(id) == True:
            note = self._swiftManager.getNote(id)
            self._readNote(note)
        else:
            print "Note #" + str(id) + " doesn't exist"

    def listNotesAndMeta(self):
        list = self._swiftManager.downloadObjectIds()
        soDict  = {}
        sort = self.settingsParser("Settings", "sort")
        for element in list:
            id = SwiftManager.objIdToId(element)
            if id is None:
                raise RuntimeError("Can not get the ID from " + element + " ... should not happen, really")
            metamngr = self._swiftManager.metaMngrFactory(element)
            id = int(id)
            crdate = metamngr.getCreateDate()
            lastmod = metamngr.getLastModifiedDate()
            tags = metamngr.getTags()
            name = SwiftManager.objIdToTitle(element)
            soDict[id] = [id, name, crdate, lastmod, tags]

        if sort == "name":
            soDict = OrderedDict(sorted(soDict.items(), key=lambda (k, v): v[1]))

        elif sort == "crdate":
            soDict = OrderedDict(sorted(soDict.items(), key=lambda (k, v): datetime.strptime(v[2], "%H:%M, %d/%m/%Y").isoformat(), reverse=True))

        elif sort == "id":
            sorted(soDict)

        else:
            soDict = OrderedDict(sorted(soDict.items(), key=lambda (k, v): datetime.strptime(v[3], "%H:%M, %d/%m/%Y").isoformat(), reverse=True))

        OutputManager.listPrint(soDict, OutputManager.HEADER_FULL)

    def settingsParser(self, section, option):
        config = ConfigParser()
        read = config.read(self._path + "/.powdernoterc")

        if read == []:
            value = "empty"
        else:
            value = config.get(section, option)

        return value

    def deleteList(self, idList):
        nameList = []
        for id in idList:
            if self._swiftManager.doesNoteExist(id) == True:
                note = self._swiftManager.getNote(id)
                title = str(note.getTitle())
                nameList.append((str(id), title))
            else:
                print "Note #" + str(id) + " doesn't exist."
                sys.exit(1)

        action = "delete note(s)"
        OutputManager.printListedNotes(nameList)
        if self._swiftManager._confirmation(action) == True:
            for id, _ in nameList:
                self._swiftManager.deleteNote(id, force=True)
            print "Ok"
        else:
            print "Abort"

    def _editNote(self, note):
        # TODO: validate note content (even if existing content coming from online should always be valid if only edited with this application)
        # raise exception if note content was not valid
        
        # TODO: edit note in a loop until the content is valid
        ret = self._editorManager.editNote(note)
        if ret == EditorManager.NEW_CONTENT_AVAILABLE:
            self._swiftManager.uploadNote(note, note.getObjectId())
            print "Note has been saved"
        else:
            print "No changes have been made, cancelling..."
            sys.exit(1)

    def searchInTitle(self, subString):
        elementList = self._searchInTitleImpl(subString)
        elementDict  = {}
        for elements in elementList:
            id = elements[0]
            elementDict[id] = elements
        sorted(elementDict)
        OutputManager.listPrint(elementDict, OutputManager.HEADER_FULL)

    def _searchInTitleImpl(self, subString):
        elementList = []
        list = self._swiftManager.downloadObjectIds()
        for element in list:
            noteId = SwiftManager.objIdToId(element)
            if noteId is None:
                raise RuntimeError("Can not get the ID from " + element + " ... should not happen, really")
            metamngr = self._swiftManager.metaMngrFactory(element)
            noteId = int(noteId)
            crdate = metamngr.getCreateDate()
            lastmod = metamngr.getLastModifiedDate()
            tags = metamngr.getTags()
            name = SwiftManager.objIdToTitle(element).lower()
            subString = subString.lower()
            loc = name.find(subString)
            if loc < 0:
                continue
            else:
                elementList.append([noteId, name, crdate, lastmod, tags])
        return elementList

    def searchInMushroom(self, substr):
        elementList = self._searchInMushroomImpl(substr)
        for element in elementList:
            OutputManager.searchMDPrint(element[0] + " - " + element[1], element[2])

    def _searchInMushroomImpl(self, substr):
        '''
        this function returns a list of lists, with the values: id, name, content
        :param substr:
        :return:
        '''
        matchstr = []
        self._swiftManager.downloadNotes()
        notes = self._swiftManager.getDownloadedNotes()
        for name, content in notes.items():
            id = SwiftManager.objIdToId(name)
            name = SwiftManager.objIdToTitle(name)
            substr = substr.lower()
            content = content.lower()
            olist = self._findMatchingIntervals(content, substr)
            if olist == []:
                continue
            else:
                intervals = []
                for alist in olist:
                    intervals.append(content[alist[0]:alist[1]])
                matchstr.append([id, name, intervals])
        return matchstr

    @staticmethod
    def _findMatchingIntervals(content, substr):
        '''
        This function searches for <substr> in <content> and returns, for each match, two indexes, the point where the
        matching start, minus a margin of 10 characters and the point where the matching ends, plus a margin of 10
        characters.
        The output is then a list of lists (list of the intervals, each one defined as a pair of [beginning, end]).
        If two or more different intervals overlap, the function merges them so that a single interval is returned
        including multiple matches. e.g.:

        "ciao" occurs on location 25, so minus the margin to the left and plus the margin to the right the index of this
        match equals [15,39]. If there is another "ciao" at location 42 the index for this match is [32, 56].
        Because this indexes overlap (32-39) the new index of the matches is [15,56]

        :param content:
        :param substr:
        :return:
        '''

        previous = -1
        current = None
        beg = None
        rightMargin = len(substr) - 1 + 15
        leftMargin = 15
        olist = []
        end = None
        prevMatch = None
        for match in Powdernote.find_all(content, substr):
            current = max(match - leftMargin, 0)
            if previous == -1:
                previous = current
                beg = previous
                prevMatch = match

            if prevMatch+rightMargin >= current:
                previous = current
                prevMatch = match
                continue
            else:
                end = min(prevMatch + rightMargin, len(content) - 1)
                previous = current
                olist.append([beg, end])
                beg = current
            prevMatch = match
        if prevMatch is not None:
            end = min(prevMatch + rightMargin, len(content) - 1)
            olist.append([beg, end])
        return olist

    @staticmethod
    def find_all(content, sub):
        start = 0
        while True:
            start = content.find(sub, start)
            if start == -1: return
            yield start
            start += len(sub) # use start += 1 to find overlapping matches

    def searchInTags(self, substr):
        '''
        for every object in list check for tags
        check if tags are the same
        if tags in element meta
        print element name
        '''

        elementList = self._searchInTagsImpl(substr)
        dict  = {}
        for elements in elementList:
            id = elements[0]
            dict[id] = elements
        sorted(dict)
        OutputManager.listPrint(dict, OutputManager.HEADER_TAG)

    def _searchInTagsImpl(self, substr):
        list = self._swiftManager.downloadObjectIds()
        elementList = []
        for element in list:
            id = SwiftManager.objIdToId(element)
            if id is None:
                raise RuntimeError("Can not get the ID from " + element + " ... should not happen, really")
            metamngr = self._swiftManager.metaMngrFactory(element)
            id = int(id)
            tags = metamngr.getTags()
            name = SwiftManager.objIdToTitle(element)
            if tags == "" or tags is None:
                continue
            tagList = tags.lower().split()
            substr = substr.lower()
            if substr in tagList:
                elementList.append([id, name, tags])
        return elementList

    def searchEverything(self, substr):
        '''
        this function searches for a substring, it doesn't matter if it is in title, content or tags, if there are results
        they will be printed.
        :param substr:
        :return:
        '''
        titleMatch = self._searchInTitleImpl(substr)
        tagMatch = self._searchInTagsImpl(substr)
        contentMatch = self._searchInMushroomImpl(substr)
        generalMatch = []

        title = {}
        tag = {}
        content = {}


        for element in titleMatch:
            title[str(element[0])] = str(element[1])

        for element in tagMatch:
            tag[str(element[0])] = [str(element[1]), element[2]]

        for element in contentMatch:
            content[str(element[0])] = [str(element[1]), element[2]]

        generalMatch = set(title.keys() + tag.keys() + content.keys())

        for element in generalMatch:
            if element in tag.keys() and element in content.keys():
                OutputManager.searchEverythingPrint(element, content[element][0], tag, content[element][1])

            elif element in content.keys():
                 OutputManager.searchEverythingPrint(element, content[element][0], None, content[element][1])

            elif element in tag.keys():
                OutputManager.searchEverythingPrint(element, tag.values()[0][0], tag.values()[0][1])

            elif element in title.keys():
                OutputManager.searchEverythingPrint(element, title.values()[0])

            else:
                print "nothing found"


    def _readNote(self, note):
        OutputManager.markdownPrint(note.getTitle(), note.getContent())

    def printMeta(self, metaId):
        if self._swiftManager.doesNoteExist(metaId) == True:
            self._swiftManager.printMeta(metaId)
        else:
            print "Note #" + str(metaId) + " doesn't exist"

    def addTags(self, tags, objId):
        self._swiftManager.addTags(tags, objId)

    def renameNote(self, noteId, newTitle):
        '''
        this function saves the note with a new title but same content and metadata to swift
        :param noteId:
        :param newTitle:
        :return:
        '''
        if self._swiftManager.doesNoteExist(noteId) == True:
            note = self._swiftManager.getNote(noteId)
            newTitle = str(noteId) + " - " + newTitle
            oldTitle = note.getObjectId()
            if oldTitle == newTitle:
                print "No changes have been made, cancelling..."
                sys.exit(1)
            self._swiftManager._renameNote(note, newTitle, oldTitle)
        else:
            print "Note #" + str(noteId) + " doesn't exist"
