from gitbro.abc.Arguments import Arguments

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
        print('this option is not mapped (yet)')

    def __run_values(self):
        print('this option is not mapped (yet)')

    def __run_default(self):
        print('this option is not mapped (yet)')

if __name__ == "__main__":
    command = Command()
    command.run()
