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

import unittest
import os
from Powdernote_impl.EditorManager import EditorManager

class EditorManager_test(unittest.TestCase):

    def test_no_initial_content_no_update(self):
        os.environ['EDITOR'] = 'TEST_---'
        em = EditorManager()
        em_ret = em._editContent()
        assert(em_ret == EditorManager.NO_NEW_CONTENT_AVAILABLE)

    def test_no_initial_content_update(self):
        os.environ['EDITOR'] = 'TEST_---newcontent'
        em = EditorManager()
        em_ret = em._editContent()
        assert(em_ret == EditorManager.NEW_CONTENT_AVAILABLE)
        assert("newcontent\n" == em.getContent())

    def test_initial_content_no_update(self):
        os.environ['EDITOR'] = 'TEST_---'
        em = EditorManager()
        em._setExistingContent("existing content")
        em_ret = em._editContent()
        assert(em_ret == EditorManager.NO_NEW_CONTENT_AVAILABLE)
        assert("existing content" == em.getContent())

    def test_initial_content_update(self):
        os.environ['EDITOR'] = 'TEST_---newcontent'
        em = EditorManager()
        em._setExistingContent("existing content")
        em_ret = em._editContent()
        assert(em_ret == EditorManager.NEW_CONTENT_AVAILABLE)
        assert("newcontent\n" == em.getContent())

if __name__ == '__main__':
    unittest.main()