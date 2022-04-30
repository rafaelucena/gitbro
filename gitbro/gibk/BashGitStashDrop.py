import os

from gitbro.abc.ListResultsCaseIgnored import ListResultsCaseIgnored

class BashGitStashDrop:
    line: str = '{base} {action} {target} {comment}' #TODO - ":extras:"
    base: str = 'git'
    action: str = 'stash drop'
    target: str = 'stash@{{{index}}}'
    question: str = 'Are you sure you want to drop the {stash_reference}? (Yy|Nn) {stash_description}'
    comment: str = ''

    def __init__(self, options: list = [], values: list = []) -> None:
        command = self.__map_command(options, values)

        #todo - colorful print - print('{0} {1} {2}'.format('\033[32mgit', self.action, 'option'))
        if not self.__confirm_just_in_case(self.target, self.comment):
            return

        print(command)
        os.system(command)

    def __confirm_just_in_case(self, reference, description):
        #TODO - get amount of stashes before printing
        answer = input(self.question.format(stash_reference=reference, stash_description=description))
        if answer == 'y' or answer == 'Y':
            return True

        return False

    def __map_command(self, options: list = [], values: list = []):
        if len(options) > 1 and options[1] == '-g':
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
        BashGitStashDrop(options, values)
