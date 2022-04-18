import os

class Command:
    def run(self):
        print('git status')
        os.system('git status')

if __name__ == "__main__":
    command = Command()
    command.run()
