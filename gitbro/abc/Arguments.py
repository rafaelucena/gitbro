import re as regex
import sys as system

class Arguments:
    def __init__(self) -> None:
        count = 0

        self.options = []
        self.values = []
        for i, command_argument in enumerate(system.argv):
            if (count == 0):
                count += 1
                continue

            if (self.__is_option(command_argument)):
                self.options.append(command_argument)
            else:
                self.values.append(command_argument)

        # print(self.values)

    def __is_option(self, command_argument: str):
        return regex.search('-\w+', command_argument)

if __name__ == "__main__":
    a = Arguments()
