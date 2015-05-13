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

import argparse
from Powdernote_impl import Powdernote

class ArgparseCommands(object):

    def __init__(self):
        super(ArgparseCommands, self).__init__()

    def commands(self):

        parser = argparse.ArgumentParser(prog="powdernote", description="powdernote")

        subparsers = parser.add_subparsers(help='powdernote Functions')

        parser_n = subparsers.add_parser('new', help='create a new note')
        parser_n.add_argument('title', type=str, help='write the title of new note')
        parser_n.set_defaults(parser_n=True)

        parser_e = subparsers.add_parser('edit', help='edit a note')
        parser_e.add_argument('e_id', type=int, help='id of note you want to edit')
        parser_e.set_defaults(parser_e=True)

        parser_l = subparsers.add_parser('list', help='lists all the notes')
        parser_l.add_argument('n_id', type=int, nargs='?', help='list information for note with given id')
        parser_l.set_defaults(parser_l=True)

        parser_d = subparsers.add_parser('delete', help='delete a note')
        parser_d.add_argument('idList', type=int, nargs='+', help='id of note you want to delete, '
                                                                  'CAUTION is recommended')
        parser_d.set_defaults(parser_d=True)

        parser_s = subparsers.add_parser('search', help='search for a SubString inside a note (searches everywhere)')
        parser_s.add_argument('-t', '--title', action='store_true', help='search in the titles of notes')
        parser_s.add_argument('-p', '--tag', action='store_true', help='search for a note with this tag')
        parser_s.add_argument('subStr', type=str, help='search for a word in a note')
        parser_s.set_defaults(parser_s=True)

        parser_r = subparsers.add_parser('read', help='display a note')
        parser_r.add_argument('r_id', type=int, help='id of note you want to read')
        parser_r.set_defaults(parser_r=True)


        parser_tag = subparsers.add_parser('tag', help='add tags to a note')
        parser_tag.add_argument('t_id', type=int, help='id of note you want to add tags to')
        parser_tag.add_argument('tagList', type=str, nargs='+', help='add tags, separate with spaces only')
        parser_tag.set_defaults(parser_tag=True)

        parser_rename = subparsers.add_parser('rename', help='rename a note')
        parser_rename.add_argument('r_id', type=int, help='id of note you want to rename')
        parser_rename.add_argument('newTitle', type=str, help='how you want to name the note')
        parser_rename.set_defaults(parser_rename=True)

        parser_history = subparsers.add_parser('history', help='versioning tools that help with checking versions, '
                                                               'diffs or deleted notes')
        parser_history.add_argument('h_id', type=int, help='list the previous versions of the note with the given ID')
        parser_history.add_argument('--read', action='store_true', help='read an older version of a note')
        parser_history.add_argument('--diff', action='store_true', help='see the diff of two notes')
        parser_history.add_argument('--restore', action='store_true', help='promote a version to the current note')
        parser_history.set_defaults(parser_history=True)

        parser_deleted = subparsers.add_parser('deleted', help='see all the backed up deleted notes')
        parser_deleted.add_argument('--undo', action='store_true', help='lets you restore a note')
        parser_deleted.set_defaults(parser_deleted=True)


        args = parser.parse_args()

        pn = Powdernote()

        if args.__contains__("parser_n"):
            note_title = args.title
            pn.newNote(note_title)

        elif args.__contains__("parser_e"):
            editId = args.e_id
            pn.editNote(editId)

        elif args.__contains__("parser_l"):
            nId = args.n_id
            if nId is not None:
                pn.printMeta(nId)
            else:
                pn.listNotesAndMeta()

        elif args.__contains__("parser_d"):
            dIdList = args.idList
            pn.deleteList(dIdList)

        elif args.__contains__("parser_s"):
            searchStr = args.subStr
            if args.title == True:
                pn.searchInTitle(searchStr)
            elif args.tag == True:
                pn.searchInTags(searchStr)
            else:
                pn.searchEverything(searchStr)

        elif args.__contains__("parser_r"):
            readId = args.r_id
            pn.readNote(readId)

        elif args.__contains__("parser_tag"):
            tags = args.tagList
            id = args.t_id
            pn.addTags(tags, id)

        elif args.__contains__("parser_rename"):
            id = args.r_id
            title = args.newTitle
            pn.renameNote(id, title)

        elif args.__contains__("parser_history"):
            id = args.h_id
            if args.read ==True:
                pn.readVersion(id)
            elif args.diff == True:
                pn.diffVersions(id)
            elif args.restore == True:
                pn.restoreVersion(id)
            else:
                pn.showHistory(id)

        elif args.__contains__("parser_deleted"):
            if args.undo == True:
                pn.undoDelete()
            else:
                pn.showDeleted()


def main():
    ac = ArgparseCommands()

    ac.commands()

if __name__ == '__main__':
    main()
