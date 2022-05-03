import re as regex
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
        return self.__prepare_case_insensitive_line_search(self.search_list, argument)

    def find_stash_list_grouped(self, argument):
        self.search_list = subprocess.getoutput('git stash list')
        return self.__prepare_stash_line_search(self.search_list, argument)

    def find_branch_by_partial(self, argument):
        self.search_list = subprocess.getoutput('git branch --no-contains')
        return self.__prepare_branch_line_search(self.search_list, argument)

    def find_last_branch_by_reflog(self):
        self.search_list = subprocess.getoutput("git reflog -1 --grep-reflog=checkout --pretty=format:'%gs'")
        return self.__prepare_branch_reflog_line(self.search_list)

    def find_first_branch_by_partial(self, argument):
        self.search_list = subprocess.getoutput('git branch -l --no-contains')
        return self.__prepare_case_insensitive_line_search(self.search_list, argument)

    def __prepare_case_insensitive_argument_search(self, argument, search_list):
        self.mapped_needles = {}
        is_case_insensitive_argument_found = False

        output_lines = self.__prepare_case_insensitive_dictionary(search_list)
        for output_line in output_lines:
            tracked_argument_case_sensitive = output_line.rfind(argument)
            if tracked_argument_case_sensitive != -1:
                return argument

            tracked_argument_case_insensitive = output_lines[output_line].rfind(argument.lower())
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

    def __prepare_case_insensitive_line_search(self, search_list, argument):
        output_lines = self.__prepare_case_insensitive_dictionary(search_list)
        for output_line in output_lines:
            tracked_argument_case_sensitive = output_line.rfind(argument)
            if tracked_argument_case_sensitive != -1:
                return output_line

            tracked_argument_case_insensitive = output_lines[output_line].rfind(argument.lower())
            if tracked_argument_case_insensitive != -1:
                return output_line

        return argument

    def __prepare_case_insensitive_dictionary(self, output: str) -> dict:
        self.parsed_lines = {}

        for output_line in output.splitlines():
            self.parsed_lines[output_line.strip()] = output_line.lower().strip()

        return self.parsed_lines

    def __prepare_stash_line_search(self, search_list, argument, search_type = 'message'): # TODO: allow stash search by branch
        stash_list = self.__prepare_stash_list_case_insensitive_dictionary(search_list)

        for stash_key in stash_list:
            tracked_argument_case_sensitive = stash_list[stash_key]['message'].rfind(argument)
            if tracked_argument_case_sensitive != -1:
                return stash_list[stash_key]

            tracked_argument_case_insensitive = stash_list[stash_key]['message_lower'].rfind(argument.lower())
            if tracked_argument_case_insensitive != -1:
                return stash_list[stash_key]

    def __prepare_stash_list_case_insensitive_dictionary(self, output):
        self.parsed_lines = {}

        stash_line = []
        for output_line in output.splitlines():
            stash_line = output_line.split(': ')

            self.parsed_lines[stash_line[0]] = {
                'stash': stash_line[0],
                'branch': stash_line[1],
                'branch_lower': stash_line[1].lower(),
                'message': stash_line[2],
                'message_lower': stash_line[2].lower(),
            }

        return self.parsed_lines

    def __prepare_branch_line_search(self, search_list, argument):
        output_lines = self.__prepare_case_insensitive_dictionary(search_list)

        for output_line in output_lines:
            tracked_argument_case_sensitive = output_line.rfind(argument)
            if tracked_argument_case_sensitive != -1:
                return output_line

            tracked_argument_case_insensitive = output_lines[output_line].rfind(argument.lower())
            if tracked_argument_case_insensitive != -1:
                return output_line

        return argument

    def __prepare_branch_reflog_line(self, search_list):
        output_line = self.__prepare_reflog_list_case_insensitive_dictionary(search_list)
        return output_line['source']

    def __prepare_reflog_list_case_insensitive_dictionary(self, output):
        self.parsed_lines = {}

        reflog_line = []
        for output_line in output.splitlines():
            reflog_line = output_line.split(': ')
            matched = regex.search('^moving from (.+) to (.+)$', reflog_line[1])

            return  {
                'acti': reflog_line[0],
                'source': matched[1],
                'source_lower': matched[1].lower(),
                'destination': matched[2],
                'destination_lower': matched[2].lower(),
            }

        return {}
