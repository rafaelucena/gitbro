import subprocess
import unittest


class GistTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(GistTestCase, self).__init__(*args, **kwargs)
        cmd = ["gist"]
        self.list_string_byte = []
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        for line in proc.stdout.readlines():
            self.list_string_byte.append(line)

    def test_find_command_in_output(self):
        command_in_output = "git status"
        find_command_in_output = [
            string_byte.decode('utf-8') for string_byte in self.list_string_byte
            if "git status" in string_byte.decode('utf-8')
        ]
        message = "Command not worked !"
        self.assertEqual(command_in_output, find_command_in_output[0].strip(), message)
        print("Command 'git status' is worked")


if __name__ == '__main__':
    unittest.main()
