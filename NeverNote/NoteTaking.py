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


from swiftclient.client import Connection
from swiftclient.client import put_object
from Configuration import Configuration
import tempfile
import os
import sys
import subprocess
import re

#   class NoteTaking(object):
#
#       def __init__(self, object_id, object_content, storage_url, token):
#           super(NoteTaking,self).__init__()
#           self._storage_url = storage_url
#           self._token = token
#           self._object_id = object_id
#           self._object_content = object_content
#
#       def getContent(self):
#           prompt = '> '
#           note_content = raw_input(prompt) #enter title, then leave 2 lines empty, then content
#           print note_content
#
#
#       def upload(self):
#           object_name = self._object_id
#           object_content = self._object_content
#           put_object(self._storage_url, self._token, Configuration.container_name, object_name, object_content)


class EditorManager(object):

    NEW_CONTENT_AVAILABLE = 1
    NO_NEW_CONTENT_AVAILABLE = 0

    TEST_CMD_PATTERN = "^TEST_"

    def __init__(self):
        super(EditorManager, self).__init__()
        self._content = None
        self._existingContent = None

    def setExistingContent(self, content):
        self._existingContent = content


    def getContent(self):
        return self._content


    def editContent(self):
        tempnote = tempfile.NamedTemporaryFile()
        if self._existingContent is not None:
            with open(tempnote.name, "w") as f:
                f.write(self._existingContent)
            oldContent = self._existingContent
        else:
            oldContent = ""
        #open tempfile with editor -> _openEditor
        self._openEditor(tempnote.name)
        #read file back
        with open(tempnote.name) as f:
            newContent = f.read()
        #check if content changed
        print newContent
        print oldContent
        self._content = newContent

        if (newContent == oldContent):
            return self.NO_NEW_CONTENT_AVAILABLE
        else:
            return self.NEW_CONTENT_AVAILABLE


    def _getEditor(self):
        '''return editor to use'''
        if sys.platform == 'plan9':
            # vi is the MIPS instruction simulator on Plan 9. We
            # instead default to E to plumb commit messages to
            # avoid confusion.
            editor = 'E'
        else:
            editor = 'vi'
        return (os.environ.get("HGEDITOR") or
                os.environ.get("VISUAL") or
                os.environ.get("EDITOR", editor))

    def _openEditor(self, filename):
        editorCmd = self._getEditor()
        if re.match(self.TEST_CMD_PATTERN, editorCmd):
            text = re.match(self.TEST_CMD_PATTERN + "---(.*)$", editorCmd).group(1)
            cmd = 'echo ' + text + ' > ' + filename
            if len(text) > 0:
                with open(filename, "w") as fn:
                    p = subprocess.Popen(cmd, shell=True, stdout=fn)
                    p.communicate()
        else:
            cmd = editorCmd.split()
            cmd.append(filename)
            editorProc = subprocess.Popen(cmd)
            editorProc.communicate()
        with open(filename) as f:
            print f.read()


def main():
    em = EditorManager()
    #em._openEditor()
    em.editContent()

if __name__ == '__main__':
    main()