import re as regex

from gitbro.abc.Arguments import Arguments
from gitbro.gilg.BashGitLogList import BashGitLogList

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
        if regex.search('^-(\d+)', self.options[0]): #logs
            BashGitLogList.go(self.options, self.values)
        elif self.options[0] == '-p': #pretty
            BashGitLogList.go(self.options, self.values)
        else:
            print('this option is not mapped (yet)')

    def __run_values(self):
        BashGitLogList.go(self.options, self.values)

    def __run_default(self):
        print('default is not mapped (yet)')

if __name__ == "__main__":
    command = Command()
    command.run()
