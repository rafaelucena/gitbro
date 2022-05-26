from gitbro.abc.Arguments import Arguments
from gitbro.gime.BashGitMergeBranch import BashGitMergeBranch
from gitbro.gime.BashGitMergeGrep import BashGitMergeGrep
from gitbro.gime.BashGitMergeLast import BashGitMergeLast

class Command:
    options: list = []
    values: list = []

    def __init__(self) -> None:
        arguments = Arguments()
        self.options = arguments.get_options()
        self.values = arguments.get_values()

    def run(self) -> None:
        if len(self.options) > 0:
            self.__run_options(self.options, self.values)
        elif len(self.values) > 0:
            self.__run_values(self.options, self.values)
        else:
            self.__run_default(self.options, self.values)

    def __run_options(self, options: list, values: list) -> None:
        if '-l' in options: #last
            BashGitMergeLast.go(options, values)
        elif '-m' in options: #master
            BashGitMergeBranch.go(options, values)
        elif '-g' in options: #grep
            BashGitMergeGrep.go(options, values)
        elif len(values) > 0: #TODO: identify and validate flags
            BashGitMergeBranch.go(self.options, self.values)
        else: # TODO: validate options
            print('This option is not mapped yet')

    def __run_values(self, options: list, values: list) -> None:
        BashGitMergeBranch.go(options, values)

    def __run_default(self, options: list, values: list) -> None:
        BashGitMergeBranch.go(options, values) #master

if __name__ == "__main__":
    command = Command()
    command.run()
