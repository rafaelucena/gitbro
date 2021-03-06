import os
import re as regex
from typing import Any
from gitbro.abc.ArgumentsParser import ArgumentsParser
from gitbro.abc.ListResultsCaseIgnored import ListResultsCaseIgnored

class BashGitBranch:
    line: str = '{base} {action} {flags} {target}' # TODO: ":extras:"
    base: str = 'git'
    action: str = 'branch'
    flags: list = []
    target: str = ''

    parser: Any
    prompt: bool = False
    question: str = ''

    # TODO: implement exclusive group on arguments parsing
    options: list = [
        {'abbrev': '', 'name': 'branch_name', 'argument': None, 'key_parameters': {'help': 'name of the branch to checkout to'}},
        {'abbrev': '-l', 'name': '-list', 'argument': False, 'key_parameters': {'help': 'list local branches'}},
        {'abbrev': '-d', 'name': '-delete', 'argument': True, 'key_parameters': {'help': 'delete a local branch', 'metavar': 'branch_name', 'type': str}},
        {'abbrev': '-g', 'name': '-grep', 'argument': True, 'key_parameters': {'help': 'partial name of the branch to checkout', 'metavar': 'partial_branch_name', 'type': str}},
        {'abbrev': '-p', 'name': '-previous', 'argument': False, 'key_parameters': {'help': 'checkout to the previous used branch'}},
        {'abbrev': '-n', 'name': '-new', 'argument': True, 'key_parameters': {'help': 'checkout to a new branch', 'metavar': 'new_branch_name', 'type': str}},
        {'abbrev': '-r', 'name': '-remotes', 'argument': False, 'key_parameters': {'help': 'list remote branches'}},
        # {'abbrev': '-t', 'name': '-terminate-branch', 'argument': True, 'key_parameters': {'help': 'delete a branch REMOTELY', 'metavar': 'branch_name', 'type': str}},
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
        self.__map_command_value(options)

        self.line = self.line.format(base=self.base, action=self.action, flags=' '.join(self.flags), target=self.target)

        return self.line

    def __map_command_options(self, options: list) -> None:
        if options.branch_name != False:
            return

        if self.parser.is_any_argument() == False:
            self.flags.append('-l')
            return

        if options.d or options.p or options.n or options.g:
            self.action = 'checkout'

            if options.n: #new
                self.flags.append('-b')
                self.target = options.n
            elif options.p: #previous
                self.target = self.__prepare_previous_branch_value()
            elif options.g: #grep
                self.target = self.__prepare_grep_branch_value(options.g)
            elif options.d: #delete
                self.prompt = True
                self.flags.append('-D')
                self.target = options.d
                self.question = 'Are you sure you want to delete the local {target}? (Yy|Nn)'.format(target=options.d)
            # elif options.t: #terminate
            #     self.prompt = True
            #     self.action = 'push origin'
            #     self.flags.append('--delete')
            #     self.target = options.t
            #     self.question = 'Are you certain you want to delete {target} remotely (THIS ACTION CANNOT BE UNDONE)? (Yy|Nn)'.format(target=options.t)

            return

        if options.l: #list
            self.flags.append('-l')

        if options.r: #remote-branches
            self.flags.append('-r')

    def __map_command_value(self, options):
        if options.branch_name:
            self.action = 'checkout'
            self.target = options.branch_name[0]

    def __prepare_grep_branch_value(self, partial_branch_name) -> str:
        branchesList = ListResultsCaseIgnored()
        value = branchesList.find_branch_by_partial(partial_branch_name)

        return value

    def __prepare_previous_branch_value(self):
        branches_list = ListResultsCaseIgnored()
        value = branches_list.find_last_branch_by_reflog()

        return value

    @staticmethod
    def go():
        BashGitBranch()
