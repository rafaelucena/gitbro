import os
import re as regex
from typing import Any
from gitbro.abc.ArgumentsParser import ArgumentsParser
from gitbro.abc.ListResultsCaseIgnored import ListResultsCaseIgnored

class BashGitMerge:
    line: str = '{base} {action} {flags} {target}' # TODO: ":extras:"
    base: str = 'git'
    action: str = 'merge'
    flags: list = []
    target: str = ''

    prompt: bool = False
    question: str = ''

    parser: Any

    # TODO: implement exclusive group on arguments parsing
    options: list = [
        # {'abbrev': '', 'name': 'partial_name', 'argument': None, 'key_parameters': {'help': 'partial name of the branch to merge'}},
        {'abbrev': '-a', 'name': '-abort', 'argument': False, 'key_parameters': {'help': 'abort the merge'}},
        {'abbrev': '-c', 'name': '-continue', 'argument': False, 'key_parameters': {'help': 'continue the merge'}},
        {'abbrev': '-d', 'name': '-dry-run', 'argument': False, 'key_parameters': {'help': 'merge the branch on a dry-run mode, without making commits'}},
        {'abbrev': '-e', 'name': '-edit-message', 'argument': False, 'key_parameters': {'help': 'edit the commit message'}},
        {'abbrev': '-i', 'name': '-ignore-message', 'argument': False, 'key_parameters': {'help': 'ignore the commit message'}},
        {'abbrev': '-l', 'name': '-last', 'argument': False, 'key_parameters': {'help': 'merge the last branch'}},
        {'abbrev': '-n', 'name': '-no-verify', 'argument': False, 'key_parameters': {'help': 'skip git hooks'}},
        {'abbrev': '-q', 'name': '-quit', 'argument': False, 'key_parameters': {'help': 'quit the merge'}},
        {'abbrev': '-s', 'name': '-stat', 'argument': False, 'key_parameters': {'help': 'show the stat'}},
        # {'abbrev': '-l', 'name': '-long', 'argument': False, 'key_parameters': {'help': 'long git status, the default of the original command'}},
        # {'abbrev': '-b', 'name': '-branch', 'argument': False, 'key_parameters': {'help': 'show the branch even on short mode'}},
        # {'abbrev': '-u', 'name': '-untracked', 'argument': False, 'key_parameters': {'help': 'see untracked files in the normal mode'}},
        # {'abbrev': '-t', 'name': '-tracked', 'argument': False, 'key_parameters': {'help': 'see tracked files only'}},
    ]

    def __init__(self) -> None:
        self.parser = ArgumentsParser(self.options)
        command = self.__map_command(self.parser.get_mapped())

        if self.prompt and not self.__confirm_just_in_case():
            return

        # TODO: colorful print - print('{0} {1} {2}'.format('\033[32mgit', self.action, 'option'))
        print(command)
        # os.system(command)

    def __confirm_just_in_case(self) -> bool:
        answer = input(self.question)
        if answer == 'y' or answer == 'Y':
            return True

        return False

    def __map_command(self, options: list) -> str:
        # self.__map_command_value(options)
        self.__map_command_options(options)

        self.line = self.line.format(base=self.base, action=self.action, flags=' '.join(self.flags), target=self.target)

        return self.line

    def __map_command_options(self, options: list) -> None:
        if options.a or options.c or options.q:
            if options.a: #abort
                self.target = '--abort'
            elif options.c: #continue
                self.target= '--continue'
            elif options.q: #quit
                self.target = '--quit'

            return

        if options.l: #last
            self.prompt = True
            self.target = self.__prepare_last_branch_value()
            self.question = 'Are you sure you want to merge the branch ({branch}) into this one? (Yy|Nn)'.format(branch=self.target)

        if options.i: #ignore (skip editing commit)
            self.flags.append('--no-edit')
        elif options.e: #edit
            self.flags.append('--edit')

        if options.s: #stat
            self.flags.append('--stat')

        if options.d: #dry-run
            self.flags.append('--no-commit')
            self.flags.append('--no-ff')

        if options.n: #no-verify (skip git hooks)
            self.flags.append('--no-verify')

    def __map_command_value(self, options):
        self.target = options.partial_name

    def __prepare_last_branch_value(self):
        branches_list = ListResultsCaseIgnored()
        value = branches_list.find_last_branch_by_reflog()

        return value

    @staticmethod
    def go():
        BashGitMerge()
