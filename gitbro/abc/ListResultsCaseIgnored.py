import subprocess

class ListResultsCaseIgnored:
    parsed_lines: dict = {}
    mapped_needles: dict = {}
    search_list: list = []

    def find_changed_files_for_diff(self, argument):
        self.search_list = subprocess.getoutput('git diff --name-only')
        return self.__prepare_case_insensitive_argument_search(argument, self.search_list)

    def find_queued_files_for_diff(self, argument):
        self.search_list = subprocess.getoutput('git diff --cached --name-only')
        return self.__prepare_case_insensitive_argument_search(argument, self.search_list)

    def find_untracked_files_for_add(self, argument):
        self.search_list = subprocess.getoutput('git ls-files --others --exclude-standard')
        return self.__prepare_case_insensitive_argument_search(argument, self.search_list)

    def find_untracked_file_for_add(self, argument):
        self.search_list = subprocess.getoutput('git ls-files --others --exclude-standard')
        return self.__prepare_case_insensitive_line_search(argument, self.search_list)

    def __prepare_case_insensitive_argument_search(self, argument, search_list):
        self.mapped_needles = {}
        is_case_insensitive_argument_found = False

        output_lines = self.__prepare_case_insensitive_dictionary(search_list)
        for output_line in output_lines:
            tracked_argument_case_sensitive = output_line.rfind(argument)
            if tracked_argument_case_sensitive != -1:
                return argument

            tracked_argument_case_insensitive = output_lines[output_line].rfind(argument)
            if tracked_argument_case_insensitive != -1:
                is_case_insensitive_argument_found = True

                needle_to_map = output_line[tracked_argument_case_insensitive:tracked_argument_case_insensitive+len(argument)]
                if needle_to_map in self.mapped_needles:
                    self.mapped_needles[needle_to_map] += 1
                else:
                    self.mapped_needles[needle_to_map] = 1

        if is_case_insensitive_argument_found == True:
            return next(iter(self.mapped_needles))

        return argument

    def __prepare_case_insensitive_line_search(self, argument, search_list):
        output_lines = self.__prepare_case_insensitive_dictionary(search_list)
        for output_line in output_lines:
            tracked_argument_case_sensitive = output_line.rfind(argument)
            if tracked_argument_case_sensitive != -1:
                return output_line

            tracked_argument_case_insensitive = output_lines[output_line].rfind(argument)
            if tracked_argument_case_insensitive != -1:
                return output_line

        return argument

    def __prepare_case_insensitive_dictionary(self, output):
        self.parsed_lines = {}

        for output_line in output.splitlines():
            self.parsed_lines[output_line] = output_line.lower()

        return self.parsed_lines
