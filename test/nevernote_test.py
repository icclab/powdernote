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

import re
import unittest
from Powdernote_impl.Note import Note
from Powdernote_impl.EditorManager import EditorManager
from Powdernote_impl.SwiftManager import SwiftManager
from Powdernote_impl.SwiftAuthManager import SwiftAuthManager
import os

class NeverNote_test(unittest.TestCase):

    def test_newNote(self):
        n = Note("test-title-abcd-#$!")
        sam = SwiftAuthManager()
        print "blabla"
        storage_url, token = sam.getcredentials()
        print "labla"
        os.environ['EDITOR'] = 'TEST_---' + n.getTitle()
        em = EditorManager()
        sm = SwiftManager(storage_url, token)
        em.editNote(n)
        print n.getContent()
        sm.uploadNote(n)
        sm.downloadNotes()
        swiftNotes = sm.getDownloadedNotes()
        found = False
        for key in swiftNotes.keys():
            if n.getTitle() in key:
                id = re.match(SwiftManager.IDREGEX, key).group(1)
                found = True
                sm.deleteNote(id)
        assert found

if __name__ == '__main__':
    unittest.main()