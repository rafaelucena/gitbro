import os
from typing import Any
from gitbro.abc.ArgumentsParser import ArgumentsParser

class BashGitCommit:
    line: str = '{base} {action} {flags} {target}' # TODO: ":extras:"
    base: str = 'git'
    action: str = 'commit'
    flags: list = []
    target: str = ''

    prompt: bool = False
    question: str = 'Are you sure you want to reset the last commit? (Yy|Nn)'

    parser: Any

    # TODO: implement exclusive group on arguments parsing
    options: list = [
        {'abbrev': '', 'name': 'commit_message', 'argument': None, 'key_parameters': {'help': 'message for the commit', 'type': str}},
        {'abbrev': '-d', 'name': '-dry-run', 'argument': False, 'key_parameters': {'help': 'dry-run the commit command'}},
        {'abbrev': '-e', 'name': '-edit-message', 'argument': False, 'key_parameters': {'help': 'edit the commit'}},
        {'abbrev': '-f', 'name': '-fix-commit', 'argument': False, 'key_parameters': {'help': 'amend|fix the last commit'}},
        {'abbrev': '-i', 'name': '-ignore-message', 'argument': False, 'key_parameters': {'help': 'ignore the interactive editor'}},
        {'abbrev': '-l', 'name': '-last-commit', 'argument': False, 'key_parameters': {'help': 'use the last commit message'}},
        {'abbrev': '-m', 'name': '-message', 'argument': True, 'key_parameters': {'help': 'message for the commit', 'action': 'extend', 'metavar': 'commit_message', 'nargs': '+', 'type': str}},
        {'abbrev': '-n', 'name': '-no-verify', 'argument': False, 'key_parameters': {'help': 'ignore git hooks'}},
        {'abbrev': '-r', 'name': '-redo-commit', 'argument': False, 'key_parameters': {'help': 'restore the last commit locally'}},
        {'abbrev': '-z', 'name': '-undo-commit', 'argument': False, 'key_parameters': {'help': 'undo|reset the last commit locally'}},
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
        self.__map_command_value(options)
        self.__map_command_options(options)

        self.line = self.line.format(base=self.base, action=self.action, flags=' '.join(self.flags), target=self.target)

        return self.line

    def __map_command_options(self, options: list) -> None:
        if self.parser.is_any_argument() == False:
            return

        if options.r or options.z:
            self.action = 'reset'

            if options.r: #redo
                self.flags.append('HEAD@{1}')
            elif options.z: #undo (ctrl+z)
                self.prompt = True
                self.target = '--soft'
                self.flags.append('HEAD~1')

            return

        if options.f: #fix
            self.flags.append('--amend')
            if options.i or options.e:
                pass
            else:
                self.flags.append('--no-edit')
        elif options.l: #last
            self.target = '-c HEAD'
        elif options.m: #message
            self.target = '-m \'' + ' '.join(options.m) + '\''

        if options.i: #ignore
            self.flags.append('--no-edit')
        elif options.e: #edit
            self.flags.append('--edit')

        if options.d: #dry-run
            self.flags.append('--dry-run')

        if options.n: #no-verify
            self.flags.append('--no-verify')

    def __map_command_value(self, options):
        if options.commit_message:
            self.target = '-m \'' + ' '.join(options.commit_message) + '\''

    @staticmethod
    def go():
        BashGitCommit()
