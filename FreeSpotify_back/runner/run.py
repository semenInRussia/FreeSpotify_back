import sys

from .main_cli_commands import MainCLICommandsCollection

commands = MainCLICommandsCollection()

def run():
    commands.run(sys.argv[1:])

if __name__ == '__main__':
    run()
