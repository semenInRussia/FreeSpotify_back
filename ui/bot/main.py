import logging

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from loguru import logger

from settings import bot
from tests.settigs_for_test import settings_with_mock
from ui.basic_ui import BasicUI

logging.basicConfig(level=logging.INFO)

_default_settings = bot


async def message_handler(message: types.Message):
    logger.debug(f"Message handler - OK, message={message.text}")

    ui = BasicUI(settings_with_mock)
    string_artist = ui.get_string_artist(message.text)

    logger.debug("Message sent!")

    await message.answer(string_artist)


class BotProgram:
    def __init__(self, additional_settings=None):
        self._init_settings(additional_settings)
        self._init_dispatcher()
        self._add_message_handler_to_dispatcher()

    def _init_settings(self, additional_settings=None):
        self._settings = _default_settings
        self._settings += additional_settings

    def _init_dispatcher(self):
        bot_ = Bot(token=self._settings.BOT_TOKEN)
        self._dispatcher = Dispatcher(bot_)

    def _add_message_handler_to_dispatcher(self):
        self._dispatcher.message_handler()(message_handler)

    def run(self):
        executor.start_polling(self._dispatcher, skip_updates=True)
