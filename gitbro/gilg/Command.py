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
        BashGitLogList.go(self.options, self.values)

if __name__ == "__main__":
    command = Command()
    command.run()
