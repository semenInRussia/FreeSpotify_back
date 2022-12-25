import os as _os
from collections import namedtuple as _namedtuple

from dotenv import load_dotenv as _load_dotenv

_load_dotenv()


BOT_TOKEN = _os.getenv('BOT_TOKEN')

BOT_NAME = "cool ROCK 'n ROLL music"

BOT_BRIEF_DESCRIPTION = (
    f"{BOT_NAME}\n Very cool bot for downloading only ROCK 'n ROLL music"
)

_BotCommand = _namedtuple("BotCommand", "name command description example")

BOT_COMMANDS = []

_BOT_COMMAND_TEXT_TEMPLATE = """
{bot_command.name} | {bot_command.command}
{bot_command.description}. For example: {bot_command.example}
\n\n
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
