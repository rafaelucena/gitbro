import argparse
from typing import Any
import re as regex
import sys as system

class ArgumentsParser():
    parser: Any = None
    mapped: Any
    unmapped: Any

    def __init__(self, options) -> None:
        self.parser = argparse.ArgumentParser(allow_abbrev=False)
        self.map_options(options)

    def map_options(self, options):
        for option in options:
            if option['argument'] == None:
                self.parser.add_argument(option['name'], nargs='*', default=False, **option['key_parameters'])
            elif option['argument'] == True:
                self.parser.add_argument(option['abbrev'], option['name'], **option['key_parameters'])
            else:
                self.parser.add_argument(option['abbrev'], option['name'], **option['key_parameters'], action='store_true')

        self.mapped, self.unmapped = self.parser.parse_known_args()

    def is_any_argument(self):
        return len(system.argv) > 1

    def get_mapped(self):
        return self.mapped

    def get_unmapped(self):
        return self.unmapped

    @staticmethod
    def __non_numeric_type(arg_value, pattern=regex.compile(r"^-[0-9]+$")):
        if not pattern.match(arg_value):
            return arg_value
