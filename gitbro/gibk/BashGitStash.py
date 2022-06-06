import os
import re as regex
from typing import Any
from gitbro.abc.ArgumentsParser import ArgumentsParser
from gitbro.abc.ListResultsCaseIgnored import ListResultsCaseIgnored

class BashGitStash:
    line: str = '{base} {action} {flags} {target} {comment}' # TODO: ":extras:"
    base: str = 'git'
    action: str = 'stash'
    flags: list = []
    target: str = ''
    comment: str = ''

    parser: Any

    # TODO: implement exclusive group on arguments parsing
    options: list = [
        {'abbrev': '', 'name': 'stash_index', 'argument': None, 'key_parameters': {'help': 'index of the stash to target'}},
        {'abbrev': '-l', 'name': '-list', 'argument': False, 'key_parameters': {'help': 'list all the stashes, with a relative date when they were created'}},
        {'abbrev': '-g', 'name': '-grep', 'argument': True, 'key_parameters': {'help': 'locate a stash by the message'}},
        {'abbrev': '-s', 'name': '-show', 'argument': True, 'key_parameters': {'help': 'view a stash with -stat (default)', 'metavar': 'stash_index', 'nargs': '?', 'default': False, 'type': str}},
        {'abbrev': '-v', 'name': '-view', 'argument': True, 'key_parameters': {'help': 'view a stash with -patch', 'metavar': 'stash_index', 'nargs': '?', 'default': False, 'type': str}},
    ]

    def __init__(self) -> None:
        self.parser = ArgumentsParser(self.options)
        command = self.__map_command(self.parser.get_mapped())

        # TODO: colorful print - print('{0} {1} {2}'.format('\033[32mgit', self.action, 'option'))
        print(command)
        os.system(command)

    def __map_command(self, options: list) -> str:
        self.__map_command_options(options)

        self.line = self.line.format(base=self.base, action=self.action, flags=' '.join(self.flags), target=self.target, comment=self.comment)

        return self.line

    def __map_command_options(self, options: list) -> None:
        if options.l or self.parser.is_any_argument() == False: #list
            self.flags.append('list')
            self.flags.append('--pretty=format:"%gd: %C(green)(%cr)%C(reset): %s"')
            return

        if options.s != False or options.v != False:
            self.flags.append('show')

            if options.v != False:
                self.flags.append('-p')

            if options.s != False and options.s != None:
                self.target = 'stash@{{{index}}}'.format(index=options.s)
                return
            elif options.v != False and options.v != None:
                self.target = 'stash@{{{index}}}'.format(index=options.v)
                return

        if options.stash_index:
            if len(self.flags) == 0:
                self.flags.append('show')

            self.target = 'stash@{{{index}}}'.format(index=options.stash_index[0])
        elif options.g:
            if len(self.flags) == 0:
                self.flags.append('show')

            list_helper = ListResultsCaseIgnored()
            stashed_item = list_helper.find_stash_list_grouped(options.g)
            if stashed_item == None:
                self.target = 'stash@{{{index}}}'.format(index=-1)
                return
            self.target = stashed_item['stash']
            self.comment = '#{branch}: {message}'.format(branch=stashed_item['branch'], message=stashed_item['message'])

    @staticmethod
    def go():
        BashGitStash()
