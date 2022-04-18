from gitbro.abc.Arguments import Arguments

class Command:
    options: list = []
    values: list = []

    def __init__(self) -> None:
        arguments = Arguments()
        self.options = arguments.get_options()
        self.values = arguments.get_values()

        # print(self.options)

    def run(self):
        if len(self.options) > 0:
            print('evaluate options')
        elif len(self.values) > 0:
            print('get to branch')

if __name__ == "__main__":
    command = Command()
    command.run()
