import re as regex
import sys as system
from typing import Any

class Arguments:
    options: list = []
    values: list = []
    matched: Any

    def __init__(self) -> None:
        if (len(system.argv) <= 1):
            return

        self.__define_options(enumerate(system.argv))

    def __define_options(self, command_arguments: enumerate):
        count = 0
        for i, command_argument in command_arguments:
            if count == 0:
                count += 1
                continue

            if self.__is_option_numeric(command_argument):
                self.options.insert(0, command_argument)
            elif self.__is_option(command_argument):
                self.options.append(command_argument)
            else:
                self.values.append(command_argument)

    def __is_option(self, command_argument: str) -> bool:
        self.matched = regex.search('^-(\w+)', command_argument)
        return type(self.matched) == regex.Match

    def __is_option_numeric(self, command_argument: str):
        self.matched = regex.search('^-(\d+)', command_argument)
        return self.matched

    def get_options(self) -> list:
        return self.options

    def get_option(self, index: int = 0) -> str:
        return self.options[index] if 0 <= index < len(self.options) else ''

    def get_values(self) -> list:
        return self.values

    def get_value(self, index: int = 0) -> str:
        return self.values[index] if 0 <= index < len(self.values) else ''

if __name__ == "__main__":
    a = Arguments()
    print(a.get_options())
