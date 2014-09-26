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
from NeverNote.NoteTaking import EditorManager

class EditorManager_test(unittest.TestCase):
    def test_editor_manager_client(self):
        os.environ['EDITOR'] = 'TEST_---'
        em = EditorManager()
        em_ret = em.editContent()
        if em_ret == EditorManager.NO_NEW_CONTENT_AVAILABLE:
            print "content didn't change"
        else:
            print "content changed"
            print em.getContent()


if __name__ == '__main__':
    unittest.main()