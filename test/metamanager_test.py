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

__author__ = 'vince'

import unittest
from mock import Mock, MagicMock, patch
from powdernote.MetaManager import MetaManager
from swiftclient.client import get_object

meta = {
    'header1': 'value1',
    'header2': 'value2',
}

class MetaManager_test(unittest.TestCase):

    def test_get_metadata(self):
        get_object = MagicMock(return_value = [meta])
        with patch('powdernote.MetaManager.get_object', get_object):
            mm = MetaManager('url', 'token', 'objectid')
            print mm._meta
            self.assertIsNone(mm._getMeta('thisdoesntexist'))
            self.assertEqual(mm._getMeta('header2'), 'value2')


if __name__ == '__main__':
    unittest.main()