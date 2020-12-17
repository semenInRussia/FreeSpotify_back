import sys
from argparse import ArgumentParser, Namespace

from loguru import logger

from server.main import app
from settings.server import PORT, HOST
from settings.general import description, epilog, help_text_for_port

parser = ArgumentParser(
    description=description,
    epilog=epilog
)

parser.add_argument('-p', '--port', '-P', type=int,
                    help=help_text_for_port,
                    default=PORT)


def run(args: list):
    args = args[1:]
    namespace: Namespace = parser.parse_args(args)

    logger.debug(namespace)

    port = namespace.port

    app.run(host=HOST,
            port=port)


if __name__ == '__main__':
    run(sys.argv)
