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

from MetaManager import MetaManager
from SwiftManager import SwiftManager
from OutputManager import OutputManager

class VersionManager(object):

        VERSIONIDENTIFIER = "v"
        DELETEIDENTIFIER = "vd"

        def __init__(self, swiftManager):
            super(VersionManager, self).__init__()
            self._swiftMngr = swiftManager

        def versionCreator(self, objectId):
            #todo: comments

            metamngr = self._swiftMngr.metaMngrFactory(objectId)
            time = metamngr.getLastModifiedDate().strftime("%Y%m%d%H%M%S%f")[:-3]
            oldTitle = objectId
            newTitle = VersionManager.VERSIONIDENTIFIER + OutputManager.DASH + time + oldTitle
            self._swiftMngr.versionUpload(oldTitle, newTitle)

