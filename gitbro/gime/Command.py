from gitbro.abc.Arguments import Arguments
from gitbro.gime.BashGitMergeActions import BashGitMergeActions
from gitbro.gime.BashGitMergeBranch import BashGitMergeBranch

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
            self.__run_values(self.options, self.values)
        else:
            self.__run_default(self.options, self.values)

    def __run_options(self, options: list, values: list):
        if self.__run_options_base_flow(options): #base flow
            BashGitMergeBranch.go(options, values)
        elif self.__run_options_actions_flow(options): #actions flow
            BashGitMergeActions.go(options, values)
        else:
            print('this option is not mapped (yet)')

    def __run_values(self, options: list, values: list):
        BashGitMergeBranch.go(options, values)

    def __run_default(self, options: list, values: list):
        BashGitMergeBranch.go(options, values) #master

    def __run_options_base_flow(self, options: list) -> bool:
        if options[0] == '-l': #last
            return True
        elif options[0] == '-g': #grep
            return True
        elif options[0] == '-m': #master
            return True

        return False

    def __run_options_actions_flow(self, options: list) -> bool:
        if options[0] == '-a': #abort
            return True
        elif options[0] == '-c': #continue
            return True
        elif options[0] == '-q': #quit
            return True

        return False

if __name__ == "__main__":
    command = Command()
    command.run()
