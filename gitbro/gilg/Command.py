import os

class Command:
    def run(self):
        print('git log')
        os.system('git log')

if __name__ == "__main__":
    command = Command()
    command.run()
