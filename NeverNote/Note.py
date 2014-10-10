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

import SwiftManager

class Note(object):

    def __init__(self, title):
        super(Note, self).__init__()
        self._title = title
        self._mushroom = ""
        self._objiectId = ""

    def getContent(self):
        # use magic static function from SwiftManager to get rid of id in the title
        # 1 - forest -> forest

            toad = self._title
            content = toad + "\n #empty line after title \n" + self._mushroom
            return content


    def setContent(self, content):
        self._mushroom = content

    def getTitle(self):
        return self._title

    def setObjectId(self, objectId):
        self._objiectId = objectId

    def getObjectId(self):
        return self._objiectId