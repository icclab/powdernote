# -*- coding: utf-8 -*-

'''
Copyright 2015 ZHAW (Zürcher Hochschule für Angewandte Wissenschaften)

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

from Configuration import Configuration
import subprocess

class KeystoneInterface(object):

    def __init__(self):
        super(KeystoneInterface, self).__init__()

    def passwordupdate(self):
        cmd = 'keystone --os-username {user} --os-password {pwd}' \
              ' --os-tenant-name {tenant} --os-auth-url {auth} password-update'.format(
                             user=Configuration.username,
                             pwd=Configuration.password,
                             tenant=Configuration.tenant_name,
                             auth=Configuration.auth_url)
        p = subprocess.Popen(cmd.split(), shell=False)
        p.communicate()
