import sys

from runner.commands_collections import CLICommandsCollection

commands = CLICommandsCollection()

if __name__ == '__main__':
    commands.run(sys.argv[1:])
