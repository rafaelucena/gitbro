import os
import re as regex
from typing import Any
from gitbro.abc.ArgumentsParser import ArgumentsParser
from gitbro.abc.ListResultsCaseIgnored import ListResultsCaseIgnored

class BashGitLog:
    line: str = '{base} {action} {flags} {target}' # TODO: ":extras:"
    base: str = 'git'
    action: str = 'log'
    flags: list = []
    target: str = ''

    parser: Any

    # TODO: implement exclusive group on arguments parsing
    options: list = [
        {'abbrev': '-a', 'name': '-author', 'argument': True, 'key_parameters': {'help': 'compare the logs with a determined branch', 'metavar': 'commit_author', 'type': str}},
        {'abbrev': '-c', 'name': '-compare', 'argument': True, 'key_parameters': {'help': 'compare the logs with a determined branch', 'metavar': 'compare_against_branch', 'type': str}},
        {'abbrev': '-d', 'name': '-diff', 'argument': False, 'key_parameters': {'help': 'see the differences into the log --patch-with-stat'}},
        {'abbrev': '-e', 'name': '-exclude-grep', 'argument': True, 'key_parameters': {'help': 'ignore logs with --invert-grep --grep', 'metavar': 'partial_search', 'type': str}},
        {'abbrev': '-g', 'name': '-grep', 'argument': True, 'key_parameters': {'help': 'track logs with --grep', 'metavar': 'partial_search', 'type': str}},
        {'abbrev': '-n', 'name': '-no-merges', 'argument': False, 'key_parameters': {'help': 'see the log without merges, --no-merges'}},
        {'abbrev': '-m', 'name': '-merges', 'argument': False, 'key_parameters': {'help': 'see the log of merges only, --merges'}},
        {'abbrev': '-o', 'name': '-oneline', 'argument': False, 'key_parameters': {'help': 'see the log with a --oneline'}},
        {'abbrev': '-p', 'name': '-pretty', 'argument': False, 'key_parameters': {'help': 'pretty log formatted'}},
        {'abbrev': '-r', 'name': '-roadmap', 'argument': False, 'key_parameters': {'help': 'see the summary of changes with --graph'}},
        {'abbrev': '-s', 'name': '-stat', 'argument': False, 'key_parameters': {'help': 'see the summary of changes with --stat'}},
    ]

    def __init__(self) -> None:
        self.parser = ArgumentsParser(self.options)
        command = self.__map_command(self.parser.get_mapped(), self.parser.get_unmapped())

        # TODO: colorful print - print('{0} {1} {2}'.format('\033[32mgit', self.action, 'option'))
        print(command)
        os.system(command)

    def __map_command(self, options: list, unmapped_options: list) -> str:
        self.__map_command_options(options)
        self.__map_command_value(options)
        self.__map_command_unmapped_options(unmapped_options)

        self.line = self.line.format(base=self.base, action=self.action, flags=' '.join(self.flags), target=self.target)

        return self.line

    def __map_command_options(self, options: list) -> None:
        if self.parser.is_any_argument() == False:
            return

        if options.a: #author
            self.flags.append('--author=\'{0}\''.format(options.a))

        if options.c: #compare
            list_results = ListResultsCaseIgnored()
            compare_against = list_results.find_branch_by_partial(options.c)
            self.flags.append('{0}..'.format(compare_against))

        if options.g: #grep
            self.flags.append('-i --grep=\'{0}\''.format(options.g))
        elif options.e: #exclude-grep
            self.flags.append('-i --grep=\'{0}\' --invert-grep'.format(options.e))

        if options.p: #pretty
            self.flags.append("--pretty=format:'%C(yellow)%h%Creset|%C(red)%ad%Creset|%C(yellow)%an%Creset:%s' --date=format:'%Y-%m-%d %H:%M:%S'")
        elif options.s: #stat
            self.flags.append('--stat')
        elif options.d: #diff
            self.flags.append('--patch-with-stat')
        elif options.o: #oneline
            self.flags.append('--oneline')

        if options.n: #no-merges
            self.flags.append('--no-merges')
        elif options.m: #merges
            self.flags.append('--merges')

        if options.r: #roadmap
            self.flags.append('--graph')

    def __map_command_value(self, options):
        pass

    def __map_command_unmapped_options(self, unmapped_options):
        for unmapped_option in unmapped_options:
            if self.target == '' and regex.search(r'^-(\d+)$', unmapped_option):
                self.target = unmapped_option

    @staticmethod
    def __non_numeric_type(arg_value, pattern=regex.compile(r"^-[0-9]+$")):
        if not pattern.match(arg_value):
            return arg_value

    @staticmethod
    def go():
        BashGitLog()
