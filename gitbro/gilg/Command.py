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
            self.__run_options(self.options, self.values)
        elif len(self.values) > 0:
            self.__run_values()
        else:
            self.__run_default()

    def __run_options(self, options: list, values: list):
        if self.__run_options_with_required_values(options):
            if len(values) == 0:
                print('You must give a partial value for the options -a, -g and -e')
            else:
                BashGitLogList.go(self.options, self.values)
        else: # TODO: validate options
            BashGitLogList.go(self.options, self.values)

    def __run_options_with_required_values(self, options: list):
        if '-a' in options: #author
            return True
        elif '-g' in options: #grep
            return True
        elif '-e' in options: #exclude
            return True

    def __run_values(self):
        BashGitLogList.go(self.options, self.values)

    def __run_default(self):
        BashGitLogList.go(self.options, self.values)

if __name__ == "__main__":
    command = Command()
    command.run()
