import logging
import re

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from loguru import logger

from settings import bot
from tests.settigs_for_test import settings_with_mock
from ui.abstract_ui import AbstractUI
from ui.basic_ui import BasicUI
from ui.statuses import Status, statuses

logging.basicConfig(level=logging.INFO)

_default_settings = bot


def _add_message_handlers_to_dispatcher(dispatcher: Dispatcher, ui: AbstractUI, settings):
    def _select_user_argument_by_message_text(message_text: str) -> str:
        res = re.search(r"/(?P<command_name>\w+)\s+(?P<argument>.+)", message_text)

        return res.group('argument')

    @dispatcher.message_handler(commands=["help"])
    async def get_bot_help_information(message: types.Message):
        await message.answer(settings.BOT_DESCRIPTION)
        await message.answer_sticker(settings.stickers.WELCOME)

    @dispatcher.message_handler(commands=["top"])
    async def message_handler(message: types.Message):
        logger.debug(f"Message handler - OK, message={message.text}")

        text_answer = _get_string_artist(message)

        await _answer_on_message(message, text_answer, ui.status)

        logger.debug("Message sent!")

    def _get_string_artist(message):
        artist_name = _select_user_argument_by_message_text(message.text)
        text_answer = ui.get_string_artist(artist_name)
        return text_answer

    async def _answer_on_message(message: types.Message, text_answer: str, status: Status):
        current_status_handler = status_handlers.get(status.value)

        await current_status_handler(message, text_answer)

    async def _answer_on_fail_message(message: types.Message, text_answer: str):
        logger.info("send FAIL result")

        await message.answer_sticker(settings.stickers.FAIL)
        await message.answer(text_answer)

    async def _answer_on_ok_message(message: types.Message, text_answer: str):
        logger.info("send GOOD result")

        await message.answer(text_answer)

    status_handlers = {
        statuses.FAIL: _answer_on_fail_message,
        statuses.OK: _answer_on_ok_message
    }


class BotProgram:
    def __init__(self, additional_settings=None):
        self._init_settings(additional_settings)
        self._init_dispatcher()
        self._init_basic_ui()

        self._add_message_handler_to_dispatcher()

    def _init_settings(self, additional_settings=None):
        self._settings = _default_settings
        self._settings += additional_settings

    def _init_dispatcher(self):
        bot_ = Bot(token=self._settings.BOT_TOKEN)

        self._dispatcher = Dispatcher(bot_)

    def _init_basic_ui(self):
        self._basic_ui = BasicUI(settings_with_mock)

    def _add_message_handler_to_dispatcher(self):
        _add_message_handlers_to_dispatcher(
            dispatcher=self._dispatcher,
            ui=self._basic_ui,
            settings=self._settings
        )

    def run(self):
        executor.start_polling(self._dispatcher, skip_updates=True)
