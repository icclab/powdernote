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

from ConfigParser import ConfigParser
from os.path import expanduser


def settingsParser(section, option):
    if Configuration.cfgcontent == []:
        value = "empty"
    else:
        value = Configuration.config.get(section, option)
    return value


class Configuration(object):

    CFG_FILE_NAME = '.powdernoterc'

    # Auth parameters
    username = ""
    password = ""
    container_name = ""
    auth_url = ""
    tenant_name = username

    # Other settings
    entriessort = ""

    config = ConfigParser()
    cfgcontent = config.read(expanduser("~") + "/{}".format(CFG_FILE_NAME))

    @staticmethod
    def initialize():
        Configuration.username = settingsParser('Auth', 'username')
        Configuration.password = settingsParser('Auth', 'password')
        Configuration.container_name = settingsParser('Auth', 'container_name')
        Configuration.auth_url = settingsParser('Auth', 'auth_url')
        Configuration.tenant_name = Configuration.username
        Configuration.entriessort = settingsParser('Settings', 'sort')

Configuration.initialize()
