from gitbro.abc.Arguments import Arguments
from gitbro.gibk.BashGitStashApply import BashGitStashApply
from gitbro.gibk.BashGitStashBoom import BashGitStashBoom
from gitbro.gibk.BashGitStashDrop import BashGitStashDrop
from gitbro.gibk.BashGitStashPop import BashGitStashPop
from gitbro.gibk.BashGitStashPush import BashGitStashPush
from gitbro.gibk.BashGitStashView import BashGitStashView

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

    def __run_options(self):
        if self.options[0] == '-n': #new|push
            BashGitStashPush.go(self.options, self.values)
        elif self.options[0] == '-c': #clear
            BashGitStashBoom.go(self.options, self.values)
        elif self.options[0] == '-d': #drop
            BashGitStashDrop.go(self.options, self.values)
        elif self.options[0] == '-a': #apply
            BashGitStashApply.go(self.options, self.values)
        elif self.options[0] == '-p': #pop
            BashGitStashPop.go(self.options, self.values)
        elif self.options[0] == '-g': #grep
            BashGitStashApply.go(self.options, self.values)
        elif self.options[0] == '-s': #stat
            BashGitStashView.go(self.options, self.values)
        elif self.options[0] == '-v': #view
            BashGitStashView.go(self.options, self.values)
        else:
            print('this option is not mapped (yet)')

    def __run_values(self):
        BashGitStashApply.go(self.options, self.values)

if __name__ == "__main__":
    command = Command()
    command.run()
