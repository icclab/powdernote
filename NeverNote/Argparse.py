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
from NeverNote import NeverNote

class ArgparseCommands(object):

    def __init__(self):
        super(ArgparseCommands, self).__init__()

    def commands(self):


        parser = argparse.ArgumentParser()

        subparsers = parser.add_subparsers(help='NeverNote Functions')

        parser_n = subparsers.add_parser('new', help='create a new note')
        parser_n.add_argument('title', type=str, help='write the title of new note')
        parser_n.set_defaults(parser_n=True)

        parser_e = subparsers.add_parser('edit', help='edit a note')
        parser_e.add_argument('e_id', type=int, help='id of note you want to edit')
        parser_e.set_defaults(parser_e=True)

        parser_l = subparsers.add_parser('list', help='lists all the notes')
        parser_l.set_defaults(parser_l=True)

        parser_d = subparsers.add_parser('delete', help='delete a note')
        parser_d.add_argument('d_id', type=int, help='id of note you want to delete, CAUTION is recommended')
        parser_d.set_defaults(parser_d=True)

        args = parser.parse_args()
        #print help(args)

        NN = NeverNote()

        if args.__contains__("parser_n"):
            note_title = args.title
            NN.newNote(note_title)

        elif args.__contains__("parser_e"):
            editId = args.e_id
            NN.editNote(editId)

        elif args.__contains__("parser_l"):
            NN.listNote()

        elif args.__contains__("parser_d"):
            deleteId = args.d_id
            NN.deleteNote(deleteId)




if __name__ == '__main__':
    ac = ArgparseCommands()

    ac.commands()