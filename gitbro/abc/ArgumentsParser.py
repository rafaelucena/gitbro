import argparse
from typing import Any

class ArgumentsParser():
    parser: Any = None
    mapped: Any
    unmapped: Any

    def __init__(self, options) -> None:
        self.parser = argparse.ArgumentParser(allow_abbrev=False)
        self.map_options(options)

    def map_options(self, options):
        for option in options:
            if option['argument']:
                self.parser.add_argument(option['abbrev'], option['name'], **option['key_parameters'])
            else:
                self.parser.add_argument(option['abbrev'], option['name'], **option['key_parameters'], action='store_true')

        self.mapped, self.unmapped = self.parser.parse_known_args()

    def get_mapped(self):
        return self.mapped

    def get_unmapped(self):
        return self.unmapped
