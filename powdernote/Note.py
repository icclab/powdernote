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


class Note(object):

    def __init__(self, title):
        super(Note, self).__init__()
        self._title = title
        self._mushroom = ""
        self._objiectId = ""

    def getContent(self):
            content = self._mushroom
            return content

    def setContent(self, content):
        '''
        When a note is created, content comes only from the editor.
        When a note is edited, content comes from Swift and from the editor

        At this point we assume that the note content is valid, this means that it
        can be of one of these formats:

        <title>
        \n
        <nothing>

        <title>
        \n
        <mushroom>

        :param content: the note content, the mushroom is an optional part of it
        '''
        self._mushroom = content

    def getTitle(self):
        return self._title

    def setObjectId(self, objectId):
        self._objiectId = objectId

    def getObjectId(self):
        return self._objiectId