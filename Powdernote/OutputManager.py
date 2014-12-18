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

class OutputManager(object):

    DASH = "-"
    BREAK = "\n"
    DOTDOTDOT = "..."
    HEADER = [["ID", "Note", "Creation Date", "Last Modified", "Tags"],["ID", "Note", "Tags"]]
    HEADER_FULL = 0
    HEADER_TAG = 1

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
