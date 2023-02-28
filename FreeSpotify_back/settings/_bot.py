import os as _os
from collections import namedtuple as _namedtuple

from dotenv import load_dotenv as _load_dotenv

_load_dotenv()


BOT_TOKEN = _os.getenv('BOT_TOKEN')

BOT_NAME = "tg bot to download a music"

BOT_BRIEF_DESCRIPTION = (
    f"{BOT_NAME}\n Very cool bot for downloading music, note that mp3 files "
    "I fetch from the https://rocknation.su , so most of the modern music "
    "isn't provided"
)

_BotCommand = _namedtuple("_BotCommand", "name command description example")

BOT_COMMANDS = [
    _BotCommand("artist",
                "/artist",
                "artist search by name",
                "/artist metallica"),
    _BotCommand("album",
                "/album",
                "album search by name",
                "/album metallica - master of puppets"),
    _BotCommand("track",
                "/track",
                "track search by name",
                "/album metallica - master of puppets")
    ]

_BOT_COMMAND_TEXT_TEMPLATE = """
{bot_command.name} | {bot_command.command}
{bot_command.description}. For example: {bot_command.example}
"""

BOT_COMMANDS_TEXT = "\n".join(
    [
        _BOT_COMMAND_TEXT_TEMPLATE.format(bot_command=bot_command)
        for bot_command in BOT_COMMANDS
    ]
)

BOT_DESCRIPTION = f"""
{BOT_BRIEF_DESCRIPTION}

COMMANDS
============================================
{BOT_COMMANDS_TEXT if BOT_COMMANDS_TEXT else "Not commands..."}
"""


class stickers:
    FAIL = (
        "CAACAgIAAxkBAAEBuVlf6MEBtd8e94ObW5LSmP1_FrWZHAACgQMAAs-71A6WvjEQeKbJyh4E"
    )
    WELCOME = (
        "CAACAgIAAxkBAAEBuVtf6MZ8_6rAiFA6uBh9uxtluKhr7wACSgEAApafjA6Mfk73uDljvh4E"
    )
