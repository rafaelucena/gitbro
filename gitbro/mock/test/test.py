import re
import subprocess
import unittest


class PackageTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(PackageTestCase, self).__init__(*args, **kwargs)
        cmd = ["pip", "list", "--format=json"]
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        for line in proc.stdout.readlines():
            self.string_byte = line
        self.string_unicode = self.string_byte.decode('utf-8')

    def test_find_package_in_pip_list(self):
        name_package = "gitbro"
        find_list_name_packages = f"{re.search(name_package, self.string_unicode)[0]}"
        message = "Package 'gitbro' not installed !"
        self.assertEqual(name_package, find_list_name_packages, message)
        print("Package 'gitbro' installed")


if __name__ == '__main__':
    unittest.main()
