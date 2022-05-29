import subprocess
import os
import re as regex
from typing import Any
from gitbro.abc.ArgumentsParser import ArgumentsParser
from gitbro.abc.ListResultsCaseIgnored import ListResultsCaseIgnored

class BashGitPush:
    line: str = '{base} {action} {flags} {target}' # TODO: ":extras:"
    base: str = 'git'
    action: str = 'push'
    flags: list = []
    target: str = ''

    parser: Any
    prompt: bool = False
    question: str = ''
    tried_output: str = ''
    suggested_command: str = ''

    # TODO: implement exclusive group on arguments parsing
    options: list = [
        {'abbrev': '-f', 'name': '-force', 'argument': False, 'key_parameters': {'help': 'force push (overwrite changes remotely)'}},
        {'abbrev': '-n', 'name': '-no-verify', 'argument': False, 'key_parameters': {'help': 'skip git hooks'}},
    ]

    def __init__(self) -> None:
        self.parser = ArgumentsParser(self.options)
        command = self.__map_command(self.parser.get_mapped())

        if self.prompt and not self.__confirm_just_in_case():
            return

        # TODO: colorful print - print('{0} {1} {2}'.format('\033[32mgit', self.action, 'option'))
        print(command)
        if and self.try_command(command) == False:
            if self.prompt and self.__confirm_just_in_case():
                self.run_suggested()

    def try_command(self, command):
        command_output = subprocess.getoutput(command)
        output_lines = command_output.splitlines()

        print(command_output)

        if regex.search('fatal: The current branch (.+) has no upstream branch', output_lines[0]):
            self.prompt = True
            self.question = 'Would you like to push and set the upstream branch? (Yy|Nn)'
            self.suggested_command = output_lines[3].strip()
            return False
        elif output_lines[0].find('fatal:') != -1:
            return False

        return True

    def run_suggested(self):
        print(self.suggested_command)
        os.system(self.suggested_command)

    def __confirm_just_in_case(self) -> bool:
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
        if self.parser.is_any_argument() == False:
            return

        if options.f: #force
            self.prompt = True
            self.question = 'The --force option will overwrite everything you have remotely, are you sure about this? (Yy|Nn)'
            self.flags.append('--force')

        if options.n: #no-verify (skip git hooks)
            self.flags.append('--no-verify')

    def __map_command_value(self, options):
        pass

    @staticmethod
    def go():
        BashGitPush()
