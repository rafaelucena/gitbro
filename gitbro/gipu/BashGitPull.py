import subprocess
import os
import re as regex
from typing import Any
from gitbro.abc.ArgumentsParser import ArgumentsParser
from gitbro.abc.ListResultsCaseIgnored import ListResultsCaseIgnored

class BashGitPull:
    line: str = '{base} {action} {flags} {target}' # TODO: ":extras:"
    base: str = 'git'
    action: str = 'pull'
    flags: list = []
    target: str = ''

    parser: Any
    prompt: bool = False
    question: str = ''
    tried_output: str = ''
    suggested_command: str = ''

    # TODO: implement exclusive group on arguments parsing
    options: list = [
        {'abbrev': '', 'name': 'branch_name', 'argument': None, 'key_parameters': {'help': 'name of the branch to pull/merge into this one'}},
        {'abbrev': '-f', 'name': '-force', 'argument': False, 'key_parameters': {'help': 'force push (overwrite changes remotely)'}},
        {'abbrev': '-u', 'name': '-set-upstream', 'argument': True, 'key_parameters': {'help': 'set upstream branch', 'metavar': 'tailored_remote_branch_name', 'nargs': '?', 'default': False, 'type': str}},
    ]

    def __init__(self) -> None:
        self.parser = ArgumentsParser(self.options)
        command = self.__map_command(self.parser.get_mapped())

        if self.prompt and not self.__confirm_just_in_case():
            return

        # TODO: colorful print - print('{0} {1} {2}'.format('\033[32mgit', self.action, 'option'))
        print(command)
        if self.try_command(command) == False:
            if self.prompt and self.__confirm_just_in_case():
                print(self.suggested_command)
                os.system(self.suggested_command)

    def try_command(self, command):
        command_output = subprocess.getoutput(command)
        output_lines = command_output.splitlines()

        print(command_output)

        if regex.search('There is no tracking information for the current branch.', output_lines[0]):
            self.prompt = True
            self.question = 'Would you like to pull and set the upstream branch? (Yy|Nn)'

            self.flags.append('--set-upstream origin')
            self.target = subprocess.getoutput('git rev-parse --abbrev-ref HEAD')

            self.suggested_command = self.line.format(base=self.base, action=self.action, flags=' '.join(self.flags), target=self.target)
            return False
        elif output_lines[0].find('fatal:') != -1:
            return False

        return True

    def __confirm_just_in_case(self) -> bool:
        answer = input(self.question)
        if answer == 'y' or answer == 'Y':
            return True

        return False

    def __map_command(self, options: list) -> str:
        self.__map_command_options(options)

        return self.line.format(base=self.base, action=self.action, flags=' '.join(self.flags), target=self.target)

    def __map_command_options(self, options: list) -> None:
        if self.parser.is_any_argument() == False:
            return

        if options.f: #force
            self.prompt = True
            self.question = 'The --force option will/might overwrite everything you have locally, are you sure about this? (Yy|Nn)'
            self.flags.append('--force')

        if options.u != False: #set-upstream
            self.target = self.__set_upstream_target(options.u)
            self.flags.append('--set-upstream origin')

    def __set_upstream_target(self, option):
        if option != None:
            return option
        else:
            return subprocess.getoutput('git rev-parse --abbrev-ref HEAD')

    @staticmethod
    def go():
        BashGitPull()
