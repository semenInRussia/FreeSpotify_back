import sys

from runner.main_cli_commands import MainCLICommandsCollection

commands = MainCLICommandsCollection()

if __name__ == '__main__':
    commands.run(sys.argv[1:])
