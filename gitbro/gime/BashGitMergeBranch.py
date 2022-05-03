import os

from gitbro.abc.ListResultsCaseIgnored import ListResultsCaseIgnored

class BashGitMergeBranch:
    line: str = '{base} {action} {flags} {target}' # TODO: ":extras:"
    base: str = 'git'
    action: str = 'merge'
    flags: list = []
    target: str = ''
    question: str = 'Are you sure you want to merge the branch ({branch}) into this one? (Yy|Nn)'

    def __init__(self, options: list = [], values: list = []) -> None:
        command = self.__map_command(options, values)

        if not self.__confirm_just_in_case():
            return

        # TODO: colorful print - print('{0} {1} {2}'.format('\033[32mgit', self.action, 'option'))
        print(command)
        os.system(command)

    def __map_command(self, options: list = [], values: list = []):
        if len(values) > 0:
            self.__map_command_values(values)

        if len(options) > 0:
            self.__map_command_options(options, values)

        if (len(options) == 0 and len(values) == 0):
            self.target = 'master'

        self.line = self.line.format(base=self.base, action=self.action, flags=' '.join(self.flags), target=self.target)

        return self.line

    def __confirm_just_in_case(self):
        answer = input(self.question.format(branch=self.target))
        if answer == 'y' or answer == 'Y':
            return True

        return False

    def __map_command_values(self, values):
        self.target = values[0]

    def __map_command_options(self, options, values):
        if '-l' == options[0] and len(values) == 0: #last
            self.target = self.__prepare_last_branch_value()
        elif '-g' == options[0]: #grep
            self.target = self.__prepare_grep_branch_value(values)
        elif '-m' == options[0]: #master
            self.target = 'master'

        if '-r' in options: #read-only (skip editing commit)
            self.flags.append('--no-edit')
        elif '-w' in options: #write (skip editing commit)
            self.flags.append('--edit')

        if '-s' in options: #stat
            self.flags.append('--stat')
        elif '-q' in options: #quiet
            self.flags.append('--quiet')

        if '-d' in options: #dry-run
            self.flags.append('--no-commit')
            self.flags.append('--no-ff')

        if '-n' in options: #no-verify (skip git hooks)
            self.flags.append('--no-verify')

    def __prepare_last_branch_value(self):
        branchesList = ListResultsCaseIgnored()
        value = branchesList.find_last_branch_by_reflog()

        return value

    def __prepare_grep_branch_value(self, values: list):
        branchesList = ListResultsCaseIgnored()
        value = branchesList.find_first_branch_by_partial(values[0])

        return value

    @staticmethod
    def go(options: list = [], values: list = []):
        BashGitMergeBranch(options, values)
