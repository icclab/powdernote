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

__author__ = 'vince'

import codecs
import os.path
import re

from powdernote.Note import Note
from powdernote.VersionManager import VersionManager
from powdernote.MetaManager import MetaManager

class ImportExportManager(object):

    TITLE_MARK = 'title'
    CONTENT_MARK = 'content'
    CRDATE_MARK = 'crdate'
    LMOD_MARK = 'lmod'
    TAGS_MARK = 'tags'

    GENERIC_RE = '^{}\[(\d+)\]$'
    TITLE_MARK_RE = GENERIC_RE.format(TITLE_MARK)
    CONTETN_MARK_RE = GENERIC_RE.format(CONTENT_MARK)
    CRDATE_MARK_RE = GENERIC_RE.format(CRDATE_MARK)
    LMOD_MARK_RE = GENERIC_RE.format(LMOD_MARK)
    TAGS_MARK_RE = GENERIC_RE.format(TAGS_MARK)

    def __init__(self, swiftmanager):
        '''
        @type swiftmanager: powdernote.SwiftManager.SwiftManager
        '''
        super(ImportExportManager, self).__init__()
        self._swiftmanager = swiftmanager
        # Maps the old id of a note with the new one after it's been imported
        self._idmapping = {}
        # List of note versions or backups to be processed after "original" notes have been imported
        self._versionordeleted = []

    def exportTo(self, filename):
        '''
        Dumps all the objects to a file
        :param filename:
        :return:
        '''
        if os.path.isfile(filename):
            print "A file named \"{}\" already exists.".format(filename)
            if not self._swiftmanager.confirmation("export notes to this file"):
                print "Operation aborted"
                return
        self._swiftmanager.downloadNotes()
        notes = self._swiftmanager.getDownloadedNotes()
        with codecs.open(filename, 'w', encoding='utf-8') as f:
            for title, content in notes.items():
                self._writeBlock(f, title, content)

    def importFrom(self, filename):
        if not os.path.isfile(filename):
            print "File \"{}\" does not exist!".format(filename)
            return
        print "WARNING: this operation will re-create powdernote notes from the ones dumped in the given file."
        print "\tNotes will not be overwritten and new IDs will be assigned randomly."
        if not self._swiftmanager.confirmation("import"):
            print "Operation aborted"
            return
        with open(filename, 'r') as f:
            while True:
                id_title, content, crdate, lmod, tags = self._readBlock(f)
                if id_title is None or content is None:
                    break
                if VersionManager.isVersionOrDeleted(id_title):
                    self._versionordeleted.append([id_title, content, crdate, lmod, tags])
                else:
                    self.uploadnewnote(id_title, content, crdate, lmod, tags)
        self._processVersionsAndDeleted()

    def _processVersionsAndDeleted(self):
        '''
        Imports versions of notes and backups, this step must be done after the source notes have alredy been
        imported
        '''
        for id_title, content, crdate, lmod, tags in self._versionordeleted:
            if VersionManager.isAnoteVersion(id_title):
                # For versions, the id of the "source" may have changed, update the title before uploading
                oldid = VersionManager.extractId(id_title)
                newid = self._idmapping[oldid]
                id_title = VersionManager.changeId(id_title, newid)
            metadict = MetaManager.getRawMetaDictionary(crdate, lmod, tags)
            self._swiftmanager.rawupload(id_title, content, metadict)

    def _tracknoteids(self, oldtitle, newtitle):
        oldid = self._swiftmanager.objIdToId(oldtitle)
        newid = self._swiftmanager.objIdToId(newtitle)
        self._idmapping[oldid] = newid

    def uploadnewnote(self, id_title, content, crdate, lmod, tags):
        note = Note(self._swiftmanager.objIdToTitle(id_title))
        note.setContent(content)
        newobjectid = self._swiftmanager.uploadNote(note, '')
        self._tracknoteids(id_title, newobjectid)
        mm = self._swiftmanager.metaManagerFactory(newobjectid)
        mm.setCreateDate(crdate)
        mm.setLastModifiedDate(lmod)
        if len(tags) > 0:
            mm.setTags(tags.split())
        mm.commitMeta()

    def _writeBlock(self, fileobject, title, content):
        '''
        Writes a block in the export file corresponding to a single note
        :param fileobject:
        :param title:
        :param content:
        :return:
        '''
        self._writegenericblock(fileobject, title, ImportExportManager.TITLE_MARK)
        self._writegenericblock(fileobject, content, ImportExportManager.CONTENT_MARK)
        mm = self._swiftmanager.metaManagerFactory(title)
        self._writegenericblock(fileobject, mm.getCreateDate(cutToSeconds=False), ImportExportManager.CRDATE_MARK)
        self._writegenericblock(fileobject, mm.getLastModifiedDate(cutToSeconds=False), ImportExportManager.LMOD_MARK)
        self._writegenericblock(fileobject, mm.getTags(), ImportExportManager.TAGS_MARK)


    def _writegenericblock(self, fileobject, content, marker):
        marker += "[{length}]\n".format(length=len(content))
        fileobject.write(marker)
        fileobject.write(content.decode('utf-8'))
        fileobject.write('\n')

    def _readBlock(self, fileobject):
        '''
        Reads a block (i.e., one single note) from an exported powdernote file
        The expected format is:
        title[<unicode length of the title>]
        <title>
        content[<unicode length of the content>]
        <content>

        @:return: two items: "ID - title" of the note and "content" of the note
        '''
        id_title = self._readgenericblock(fileobject, ImportExportManager.TITLE_MARK_RE)
        content = self._readgenericblock(fileobject, ImportExportManager.CONTETN_MARK_RE)
        crdate = self._readgenericblock(fileobject, ImportExportManager.CRDATE_MARK_RE)
        lmod = self._readgenericblock(fileobject, ImportExportManager.LMOD_MARK_RE)
        tags = self._readgenericblock(fileobject, ImportExportManager.TAGS_MARK_RE)
        return id_title, content, crdate, lmod, tags

    def _readgenericblock(self, fileobject, mark_regex):
        '''
        A block is made of:
        marker[length]
        <text>
        The provided mark_regex is a regex that will extract the length when applied to the line of text containing the
        marker
        :return: the text extracted from the block
        '''
        mark = fileobject.readline()
        if len(mark) == 0:
            return None
        try:
            length = re.match(mark_regex, mark).group(1)
        except AttributeError:
            print "Unexpected format of content marker at line \"{}\"... aborting".format(mark)
            return None
        text = fileobject.read(int(length)).decode('utf-8')
        # skip the new line
        fileobject.read(1)
        return text
