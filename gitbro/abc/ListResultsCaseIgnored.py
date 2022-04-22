import subprocess

class ListResultsCaseIgnored:
    parsed_lines: dict = {}
    mapped_needles: dict = {}
    search_list: list = []

    def find_changed_files_for_diff(self, argument):
        self.search_list = subprocess.getoutput('git diff --name-only')
        return self.__prepare_case_insensitive_argument_search(argument, self.search_list)

    def __prepare_case_insensitive_argument_search(self, argument, search_list):
        self.parsed_lines = {}
        self.mapped_needles = {}
        is_case_insensitive_argument_found = False

        for changed_line in search_list.splitlines():
            self.parsed_lines[changed_line] = changed_line.lower()

            tracked_argument_case_sensitive = changed_line.rfind(argument)
            if tracked_argument_case_sensitive != -1:
                return argument

            tracked_argument_case_insensitive = self.parsed_lines[changed_line].rfind(argument)
            if tracked_argument_case_insensitive != -1:
                is_case_insensitive_argument_found = True

                needle_to_map = changed_line[tracked_argument_case_insensitive:tracked_argument_case_insensitive+len(argument)]
                if needle_to_map in self.mapped_needles:
                    self.mapped_needles[needle_to_map] += 1
                else:
                    self.mapped_needles[needle_to_map] = 1

        if is_case_insensitive_argument_found == True:
            return next(iter(self.mapped_needles))

        return argument
