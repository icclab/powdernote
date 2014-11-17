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


import tempfile
import os
import sys
import subprocess
import re



class EditorManager(object):
    '''
    Handles an editing session: starts an editor and collect input from the user.
    Editors can also have an initial existing content.
    '''

    NEW_CONTENT_AVAILABLE = 1
    NO_NEW_CONTENT_AVAILABLE = 0

    TEST_CMD_PATTERN = "^TEST_"

    def __init__(self):
        super(EditorManager, self).__init__()
        self._content = None
        self._existingContent = None


    def _setExistingContent(self, content):
        '''
        :param content: initial content to be used when the editing session will start
        '''
        if len(content) > 0:
            self._existingContent = content


    def getContent(self):
        '''
        :return: the content of the editor manager, can be empty, not-initialized, un-updated, ...
        '''
        #print "getContent: {}".format(self._content)
        return self._content


    def _editContent(self):
        '''
        Edits the content.
        :return: NEW_CONTENT_AVAILABLE if content was updated, NO_NEW_CONTENT_AVAILABLE otherwise
        '''
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

        self._content = newContent

        if (newContent == oldContent):
            return self.NO_NEW_CONTENT_AVAILABLE
        else:
            return self.NEW_CONTENT_AVAILABLE


    def editNote(self, note):
        '''
        Starts an editing session on a note object (initial content will be the note content)
        :param note: note object to be edited
        :return: NEW_CONTENT_AVAILABLE if the note was changed
        '''
        self._setExistingContent(note.getContent())

        ret = self._editContent()

        if ret is self.NEW_CONTENT_AVAILABLE:
            content = self.getContent()
            note.setContent(content)

        return ret


    def _getEditor(self):
        '''return editor to use'''
        if sys.platform == 'plan9':
            # vi is the MIPS instruction simulator on Plan 9. We
            # instead default to E to avoid confusion.
            editor = 'E'
        else:
            editor = 'vi'
        return (os.environ.get("VISUAL") or
                os.environ.get("EDITOR", editor))

    def _openEditor(self, filename):
        '''
        Runs the editor on the given file name
        '''
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