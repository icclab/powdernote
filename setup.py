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

from setuptools import setup

setup(name='powdernote',
      version='1.0',
      description='Powdernote',
      author='The Kid',
      author_email='anke@zhaw.ch',
      url='http://blog.zhaw.ch/icclab',
      license='Apache 2.0',
      packages=['Powdernote'],
      install_requires=['tabulate', 'python-swiftclient'],
      entry_points={'console_scripts':['powdernote = powdernote.__main__:main']}
)