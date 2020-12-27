import os

from dotenv import load_dotenv

load_dotenv()

BOT_NAME = "Music manager [FREE]"

BOT_TOKEN = os.getenv('BOT_TOKEN')

BOT_DESCRIPTION = """I am very COOL bot. My name is {name} and I can taking Rock n' Roll music.""".format(name=BOT_NAME)


class stickers:
    FAIL = "CAACAgIAAxkBAAEBuVlf6MEBtd8e94ObW5LSmP1_FrWZHAACgQMAAs-71A6WvjEQeKbJyh4E"
    WELCOME = "CAACAgIAAxkBAAEBuVtf6MZ8_6rAiFA6uBh9uxtluKhr7wACSgEAApafjA6Mfk73uDljvh4E"
