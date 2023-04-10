import sys

from FreeSpotify_back.runner.main_cli_commands import MainCLICommandsCollection

commands = MainCLICommandsCollection()

def run() -> None:
    """Run the project using the accepted from command line arguments."""
    commands.run(sys.argv[1:])

if __name__ == '__main__':
    run()
