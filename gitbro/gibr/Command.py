from gitbro.abc.Arguments import Arguments
from gitbro.gibr.BashGitBranchDelete import BashGitBranchDelete
from gitbro.gibr.BashGitBranchKill import BashGitBranchKill
from gitbro.gibr.BashGitBranchList import BashGitBranchList
from gitbro.gibr.BashGitBranchSet import BashGitBranchSet

class Command:
    options: list = []
    values: list = []

    def __init__(self) -> None:
        arguments = Arguments()
        self.options = arguments.get_options()
        self.values = arguments.get_values()

    def run(self):
        if len(self.options) > 0:
            self.__run_options()
        elif len(self.values) > 0:
            self.__run_values()
        else:
            self.__run_default()

    def __run_options(self):
        if self.options[0] == '-d':
            BashGitBranchDelete.go(self.options, self.values)
        elif self.options[0] == '-k':
            BashGitBranchKill.go(self.options, self.values)
        elif self.options[0] == '-l':
            BashGitBranchList.go(self.options, self.values)
        elif self.options[0] == '-g':
            print('track a branch by a partial string')
        elif self.options[0] == '-r':
            print('track the last used branch and return to it')
        else:
            print('this option is not mapped (yet)')

    def __run_values(self):
        BashGitBranchSet.go(self.options, self.values)

    def __run_default(self):
        BashGitBranchList.go(self.options, self.values)

if __name__ == "__main__":
    command = Command()
    command.run()
