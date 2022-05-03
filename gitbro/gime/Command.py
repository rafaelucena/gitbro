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
            self.__run_options()
        elif len(self.values) > 0:
            self.__run_values()
        else:
            self.__run_default()

    def __run_options(self):
        if self.__run_options_base_flow(self.options): #base flow
            BashGitMergeBranch.go(self.options, self.values)
        elif self.__run_options_actions_flow(self.options): #actions flow
            BashGitMergeActions.go(self.options, self.values)
        else:
            print('this option is not mapped (yet)')

    def __run_options_base_flow(self, options):
        if options[0] == '-l': #last
            return True

        return False

    def __run_options_actions_flow(self, options):
        if options[0] == '-a': #abort
            return True
        elif options[0] == '-c': #continue
            return True
        elif options[0] == '-q': #quit
            return True

        return False

    def __run_values(self):
        BashGitMergeBranch.go(self.options, self.values)

    def __run_default(self):
        # TODO: define default for gime command
        print('default is not mapped (yet)')

if __name__ == "__main__":
    command = Command()
    command.run()
