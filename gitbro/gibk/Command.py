import os

class Command:
    def run(self):
        print('git stash list')
        os.system('git stash list')

if __name__ == "__main__":
    command = Command()
    command.run()
