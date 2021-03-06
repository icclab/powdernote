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

import unittest
from Powdernote_impl.Powdernote_impl import Powdernote


class MushroomSearch_Test(unittest.TestCase):

    marginLeft = 10
    marginRight = 10

    # search: ciao
    input1 = "aaa aaa ciao ciao"
    expected1 = [[0, len(input1) - 1]]

    # search: ciao
    input2 = "aaa aaa aaa ciao aaa aaa aaa ciao ciao aaa aaa aaa aaa"
    expected2 = [[2, 47]]

    input3 = "aaa aaa aaa ciao aaa aaa aaa aaa aaa aaa aaa aaa ciao"
    expected3 = [[2, 25], [39, len(input3) - 1]]

    input4 = "aaa aaa ciao aaa ciao aaa aaa aaa aaa aaa aaa ciao aaa gdfgdfgdfgdfgdfgdfgdfgdfgdfgdfgdfg ciao aaaaaa"
    expected4 = [[0, 30], [36, 59], [80, 100]]

    def searchInMushroom(self, string, keyword):
        olist = Powdernote._findMatchingIntervals(string, keyword)
        return olist

    def test_mushroomSearch(self):
        indexes = self.searchInMushroom(self.input1, "ciao")
        print indexes, self.expected1
        assert(indexes == self.expected1)

        indexes = self.searchInMushroom(self.input2, "ciao")
        print indexes, self.expected2
        assert(indexes == self.expected2)

        indexes = self.searchInMushroom(self.input3, "ciao")
        print indexes, self.expected3
        assert(indexes == self.expected3)

        indexes = self.searchInMushroom(self.input4, "ciao")
        print indexes, self.expected4
        assert(indexes == self.expected4)
