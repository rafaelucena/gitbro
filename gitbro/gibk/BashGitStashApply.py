import os
from gitbro.abc.ListResultsCaseIgnored import ListResultsCaseIgnored

class BashGitStashApply:
    line: str = '{base} {action} {target} {comment}' # @todo - ":extras:"
    base: str = 'git'
    action: str = 'stash apply'
    target: str = 'stash@{{{index}}}'
    comment: str = ''

    def __init__(self, options: list = [], values: list = []) -> None:
        command = self.__map_command(options, values)

        # @todo - colorful print - print('{0} {1} {2}'.format('\033[32mgit', self.action, 'option'))
        print(command)
        # os.system(command)

    def __map_command(self, options: list = [], values: list = []):
        if len(options) > 0 and options[0] == '-g':
            list_helper = ListResultsCaseIgnored()
            stashed_item = list_helper.find_stash_list_grouped(values[0])
            self.target = stashed_item['stash']
            self.comment = '#{branch}: {message}'.format(branch=stashed_item['branch'], message=stashed_item['message'])
        else:
            self.target = self.target.format(index=values[0])

        self.line = self.line.format(base=self.base, action=self.action, target=self.target, comment=self.comment)

        return self.line

    @staticmethod
    def go(options: list = [], values: list = []):
        BashGitStashApply(options, values)