from gitbro.abc.Arguments import Arguments
from gitbro.gibk.BashGitStashApply import BashGitStashApply
from gitbro.gibk.BashGitStashBoom import BashGitStashBoom
from gitbro.gibk.BashGitStashList import BashGitStashList
from gitbro.gibk.BashGitStashPush import BashGitStashPush

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
        if self.options[0] == '-s':
            BashGitStashPush.go(self.options, self.values)
        elif self.options[0] == '-c':
            BashGitStashBoom.go(self.options, self.values)
        elif self.options[0] == '-l':
            BashGitStashList.go(self.options, self.values)
        elif self.options[0] == '-g':
            BashGitStashApply.go(self.options, self.values)
        else:
            print('this option is not mapped (yet)')

    def __run_values(self):
        BashGitStashApply.go(self.options, self.values)

    def __run_default(self):
        BashGitStashList.go(self.options, self.values)

if __name__ == "__main__":
    command = Command()
    command.run()
