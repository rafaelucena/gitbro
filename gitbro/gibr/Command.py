import os

class Command:
    def run(self):
        print('git branch')
        os.system('git branch')

if __name__ == "__main__":
    command = Command()
    command.run()
