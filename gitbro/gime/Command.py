import os

class Command:
    def run(self):
        print('git merge')
        os.system('git merge')

if __name__ == "__main__":
    command = Command()
    command.run()
