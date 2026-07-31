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
    prompt: bool = False
    question: str = ''

    # TODO: implement exclusive group on arguments parsing
    options: list = [
        {'abbrev': '', 'name': 'stash_index', 'argument': None, 'key_parameters': {'help': 'index of the stash to target'}},
        {'abbrev': '-a', 'name': '-apply', 'argument': True, 'key_parameters': {'help': 'apply a stash', 'metavar': 'stash_index', 'nargs': '?', 'default': False, 'type': str}},
        {'abbrev': '-c', 'name': '-clear', 'argument': False, 'key_parameters': {'help': 'clear all the stashes'}},
        {'abbrev': '-d', 'name': '-drop', 'argument': True, 'key_parameters': {'help': 'drop a stash', 'metavar': 'stash_index', 'nargs': '?', 'default': False, 'type': str}},
        {'abbrev': '-g', 'name': '-grep', 'argument': True, 'key_parameters': {'help': 'locate a stash by the message', 'metavar': 'stash_message'}},
        {'abbrev': '-l', 'name': '-list', 'argument': False, 'key_parameters': {'help': 'list all the stashes, with a relative date when they were created'}},
        {'abbrev': '-n', 'name': '-new', 'argument': True, 'key_parameters': {'help': 'push the local changes into a new stash', 'metavar': 'stash_message', 'nargs': '?', 'default': False, 'type': str}},
        {'abbrev': '-p', 'name': '-pop', 'argument': True, 'key_parameters': {'help': 'pop a stash', 'metavar': 'stash_index', 'nargs': '?', 'default': False, 'type': str}},
        {'abbrev': '-s', 'name': '-show', 'argument': True, 'key_parameters': {'help': 'view a stash with -stat (default)', 'metavar': 'stash_index', 'nargs': '?', 'default': False, 'type': str}},
        {'abbrev': '-v', 'name': '-view', 'argument': True, 'key_parameters': {'help': 'view a stash with -patch', 'metavar': 'stash_index', 'nargs': '?', 'default': False, 'type': str}},
    ]

    def __init__(self) -> None:
        self.parser = ArgumentsParser(self.options)
        command = self.__map_command(self.parser.get_mapped())

        if self.prompt and not self.__confirm_just_in_case():
            return

        # TODO: colorful print - print('{0} {1} {2}'.format('\033[32mgit', self.action, 'option'))
        print(command)
        os.system(command)

    def __confirm_just_in_case(self):
        answer = input(self.question)
        if answer == 'y' or answer == 'Y':
            return True

        return False

    def __map_command(self, options: list) -> str:
        self.__map_command_options(options)

        self.line = self.line.format(base=self.base, action=self.action, flags=' '.join(self.flags), target=self.target, comment=self.comment)

        return self.line

    def __map_command_options(self, options: list) -> None:
        if options.l or self.parser.is_any_argument() == False: #list
            self.flags.append('list')
            self.flags.append('--pretty=format:"%gd: %C(green)(%cr)%C(reset): %s"')
            return

        if options.n != False:
            self.flags.append('push')

            if options.n != None:
                self.flags.append('-m')
                self.target = options.n

            return
        elif options.c:
            self.prompt = True
            # TODO: get amount of stashes before printing
            self.question = 'Are you sure you want to delete all the stashes? (Yy|Nn)'

            self.flags.append('clear')
            return
        elif options.d != False:
            self.prompt = True
            # TODO: tailor the question to the stash expected to be dropped
            self.question = 'Are you sure you want to drop the stash? (Yy|Nn)'

            self.flags.append('drop')

            if self.__map_command_option_if_present(options.d):
                return
        elif options.s != False or options.v != False: #show|view
            self.flags.append('show')

            if options.v != False: #view
                self.flags.append('-p')

            if self.__map_command_option_if_present(options.s):
                return
            elif self.__map_command_option_if_present(options.v):
                return
        elif options.a != False: #apply
            self.flags.append('apply')

            if self.__map_command_option_if_present(options.a):
                return
        elif options.p != False: #pop
            self.flags.append('pop')

            if self.__map_command_option_if_present(options.p):
                return

        if options.stash_index:
            if len(self.flags) == 0:
                self.flags.append('show')

            self.target = 'stash@{{{index}}}'.format(index=options.stash_index[0])
        elif options.g: #grep
            if len(self.flags) == 0:
                self.flags.append('show')

            list_helper = ListResultsCaseIgnored()
            stashed_item = list_helper.find_stash_list_grouped(options.g)
            if stashed_item == None:
                self.target = 'stash@{{{index}}}'.format(index=-1)
                return
            self.target = stashed_item['stash']
            self.comment = '#{branch}: {message}'.format(branch=stashed_item['branch'], message=stashed_item['message'])

    def __map_command_option_if_present(self, option):
        if option != False and option != None:
            self.target = 'stash@{{{index}}}'.format(index=option)
            return True

        return False

    @staticmethod
    def go():
        BashGitStash()
