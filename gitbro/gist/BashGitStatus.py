import os
from gitbro.abc.ArgumentsParser import ArgumentsParser
from gitbro.abc.ListResultsCaseIgnored import ListResultsCaseIgnored

class BashGitStatus:
    line: str = '{base} {action} {flags} {target}' # TODO: ":extras:"
    base: str = 'git'
    action: str = 'status'
    flags: list = []
    target: str = ''

    options: list = [
        {'abbrev': '-s', 'name': '-short', 'argument': False, 'key_parameters': {'help': 'short'}},
        {'abbrev': '-g', 'name': '-grep', 'argument': True, 'key_parameters': {'help': 'grep', 'metavar': 'partial_name', 'dest': 'partial'}},
    ]

    def __init__(self) -> None:
        parser = ArgumentsParser(self.options)
        command = self.__map_command(parser.get_mapped())

        # TODO: colorful print - print('{0} {1} {2}'.format('\033[32mgit', self.action, 'option'))
        print(command)
        os.system(command)

    def __map_command(self, options: list) -> str:
        self.__map_command_options(options)

        self.line = self.line.format(base=self.base, action=self.action, flags=' '.join(self.flags), target=self.target)

        return self.line

    def __map_command_options(self, options: list) -> None:
        if options.s:
            self.flags.append('--short')

    @staticmethod
    def go():
        BashGitStatus()
