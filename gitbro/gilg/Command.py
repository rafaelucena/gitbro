from gitbro.abc.Arguments import Arguments
from gitbro.gilg.BashGitLogAuthor import BashGitLogAuthor
from gitbro.gilg.BashGitLogCompare import BashGitLogCompare

class Command:
    options: list = []
    values: list = []

    def __init__(self) -> None:
        arguments = Arguments()
        self.options = arguments.get_options()
        self.values = arguments.get_values()

    def run(self):
        if len(self.options) > 0:
            self.__run_options(self.options, self.values)

    def __run_options(self, options: list, values: list):
        if '-a' in options: #author
            BashGitLogAuthor.go(options, values)
        elif '-c' in options: #exclude
            BashGitLogCompare.go(options, values)

if __name__ == "__main__":
    command = Command()
    command.run()
