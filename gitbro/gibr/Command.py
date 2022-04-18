import os
from gitbro.abc.Arguments import Arguments
from gitbro.gibr.BashGitNewBranch import BashGitNewBranch
from gitbro.gibr.BashGitSetBranch import BashGitSetBranch

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
        if self.options[0] == '-n':
            BashGitNewBranch.go(self.options, self.values)

    def __run_values(self):
        BashGitSetBranch.go(self.options, self.values)

    def __run_default(self):
        print('git branch')
        os.system('git branch')

if __name__ == "__main__":
    command = Command()
    command.run()
