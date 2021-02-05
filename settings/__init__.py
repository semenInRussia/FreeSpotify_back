from settings_master import Settings

from settings import bot as _bot
from settings import entities as _entities
from settings import main as _main
from settings import server as _server
from settings import spotify as _spotify

main = Settings(_main)
bot = Settings(_bot)
entities = Settings(_entities)
spotify = Settings(_spotify)
server = Settings(_server)
