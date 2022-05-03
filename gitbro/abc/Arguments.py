import re as regex
import sys as system

class Arguments:
    options: list = []
    values: list = []

    def __init__(self) -> None:
        if (len(system.argv) <= 1):
            return

        self.__define_options(enumerate(system.argv))

    def __define_options(self, command_arguments: enumerate):
        count = 0
        for i, command_argument in command_arguments:
            if (count == 0):
                count += 1
                continue

            if (self.__is_option(command_argument)):
                self.options.append(command_argument)
            else:
                self.values.append(command_argument)

    def __is_option(self, command_argument: str):
        return regex.search('^-\w+', command_argument)

    def get_options(self, index: int = None):
        if (index is not None):
            return self.options[index] if 0 <= index < len(self.options) else None

        return self.options

    def get_values(self, index: int = None):
        if (index is not None):
            return self.values[index] if 0 <= index < len(self.values) else None

        return self.values

if __name__ == "__main__":
    a = Arguments()
    print(a.get_options())
