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

from tabulate import tabulate
from difflib import ndiff

class OutputManager(object):

    DASH = "-"
    BREAK = "\n"
    DOTDOTDOT = "..."
    HEADER = [["ID", "Note", "Creation Date", "Last Modified", "Tags"],["ID", "Note", "Tags"], ["ID", "Note"], ["ID", "Version", "Title"]]
    HEADER_FULL = 0
    HEADER_TAG = 1
    HEADER_TITLEID = 2
    ID_TITLE_SEPERATOR = " - "

    def __init__(self):
        super(OutputManager, self).__init__()
        raise Exception("this object should not be instantiated")

    @staticmethod
    def listPrint(dict, header):
        table = []
        for value in dict.values():
            table.append(value)
        print tabulate(table, headers=OutputManager.HEADER[header])

    @staticmethod
    def _markdownPrint(title, content):
        print title + OutputManager.BREAK + OutputManager.DASH * len(title) + OutputManager.BREAK + content + \
              OutputManager.BREAK

    @staticmethod
    def markdownPrint(title, content):
        OutputManager._markdownPrint(title, content)

    @staticmethod
    def searchMDPrint(title, content):
        string = ""
        for match in content:
            string = string + OutputManager.DOTDOTDOT + match.replace("\n", " ") + OutputManager.DOTDOTDOT + OutputManager.BREAK
        OutputManager._markdownPrint(title, string)

    @staticmethod
    def printListedNotes(noteList):
        for id, title in noteList:
            print id + OutputManager.ID_TITLE_SEPERATOR + title

    @staticmethod
    def searchEverythingPrint(id, title, tag = None, content = None):

        if tag is None and content is None:
            print id + OutputManager.ID_TITLE_SEPERATOR + title

        elif tag is not None and content is None:
            print id + OutputManager.ID_TITLE_SEPERATOR + title + OutputManager.BREAK + "    Tags: " + str(tag) + OutputManager.BREAK

        elif tag is None and content is not None:
            title = id + OutputManager.ID_TITLE_SEPERATOR + title
            OutputManager.searchMDPrint(title, content)

        elif tag is not None and content is not None:
            title = id + OutputManager.ID_TITLE_SEPERATOR + title
            OutputManager.searchMDPrint(title, content)
            print "Tags: " + str(tag[id][1]) + OutputManager.BREAK


    @staticmethod
    def printDiff(content1, content2):
        '''
        prints the diff of two strings
        :param content1:
        :param content2:
        :return:
        '''
        diff = ndiff(content1.splitlines(), content2.splitlines())
        print '\n'.join(list(diff))
