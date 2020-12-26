import os

from dotenv import load_dotenv

load_dotenv()

BOT_NAME = "Music manager [FREE]"

BOT_TOKEN = os.getenv('BOT_TOKEN')

BOT_DESCRIPTION = """I am very COOL bot. My name is {name} and I can taking Rock n' Roll music.""".format(name=BOT_NAME)
