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
from Powdernote import Powdernote

class ArgparseCommands(object):

    def __init__(self):
        super(ArgparseCommands, self).__init__()

    def commands(self):

        parser = argparse.ArgumentParser(prog="Powdernote", description="Powdernote")

        subparsers = parser.add_subparsers(help='Powdernote Functions')

        parser_n = subparsers.add_parser('new', help='create a new note')
        parser_n.add_argument('title', type=str, help='write the title of new note')
        parser_n.set_defaults(parser_n=True)

        parser_e = subparsers.add_parser('edit', help='edit a note')
        parser_e.add_argument('e_id', type=int, help='id of note you want to edit')
        parser_e.set_defaults(parser_e=True)

        parser_l = subparsers.add_parser('list', help='lists all the notes')
        parser_l.add_argument('-l', '--list_details', action='store_true', help='list all notes with meta data')
        parser_l.set_defaults(parser_l=True)

        parser_d = subparsers.add_parser('delete', help='delete a note')
        parser_d.add_argument('d_id', type=int, help='id of note you want to delete, CAUTION is recommended')
        parser_d.set_defaults(parser_d=True)

        # search -c ravioli
        parser_s = subparsers.add_parser('search', help='search for a SubString inside a note (will only search in titles)')
        parser_s.add_argument('-c', '--content', action='store_true', help='search in the content of a note')
        parser_s.add_argument('-t', '--tag', action='store_true', help='search for note with this tag')
        parser_s.add_argument('subStr', type=str, help='search for a word in a title')
        parser_s.set_defaults(parser_s=True)

        parser_r = subparsers.add_parser('read', help='display a note')
        parser_r.add_argument('r_id', type=int, help='id of note you want to read')
        parser_r.set_defaults(parser_r=True)

        parser_md = subparsers.add_parser('meta', help='get meta')
        parser_md.add_argument('md_id', type=int, help='id of note you want metadata from')
        parser_md.set_defaults(parser_md=True)

        parser_tag = subparsers.add_parser('tag', help='add tags to a note')
        parser_tag.add_argument('t_id', type=int, help='id of note you want to add tags to')
        parser_tag.add_argument('tagList', type=str, nargs='+', help='add tags, seperate with spaces only')
        parser_tag.set_defaults(parser_tag=True)


        args = parser.parse_args()
        #print help(args)

        pn = Powdernote()

        if args.__contains__("parser_n"):
            note_title = args.title
            pn.newNote(note_title)

        elif args.__contains__("parser_e"):
            editId = args.e_id
            pn.editNote(editId)

        elif args.__contains__("parser_l"):
            pn.listNotesAndMeta()

        elif args.__contains__("parser_d"):
            deleteId = args.d_id
            pn.deleteNote(deleteId)

        elif args.__contains__("parser_s"):
            searchStr = args.subStr
            if args.content == True:
                pn.searchInMushroom(searchStr)
            elif args.tag == True:
                pn.searchInTags(searchStr)
            else:
                pn.searchInTitle(searchStr)

        elif args.__contains__("parser_r"):
            readId = args.r_id
            pn.readNote(readId)

        elif args.__contains__("parser_md"):
            metaId = args.md_id
            pn.printMeta(metaId)

        elif args.__contains__("parser_tag"):
            tags = args.tagList
            id = args.t_id
            pn.addTags(tags, id)


if __name__ == '__main__':
    ac = ArgparseCommands()

    ac.commands()