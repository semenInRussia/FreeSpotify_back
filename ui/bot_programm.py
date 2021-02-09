import logging

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from loguru import logger

from settings import bot
from tests.settigs_for_test import settings_with_mock
from ui.basic_ui import BasicUI
from ui.statuses import Status, statuses

logging.basicConfig(level=logging.INFO)

_default_settings = bot


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
        @self._dispatcher.message_handler()
        async def message_handler(message: types.Message):
            logger.debug(f"Message handler - OK, message={message.text}")

            text_answer = self._basic_ui.get_string_artist(message.text)

            await self._answer_on_message(message, text_answer, status=self._basic_ui.status)

            logger.debug("Message sent!")

    @property
    def status_handlers(self):
        return {
            statuses.FAIL: self._answer_on_fail_message,
            statuses.OK: self._answer_on_ok_message
        }

    async def _answer_on_message(self, message: types.Message, text_answer: str, status: Status):
        current_status_handler = self.status_handlers.get(status.value)

        await current_status_handler(message, text_answer)

    async def _answer_on_fail_message(self, message: types.Message, text_answer: str):
        await message.answer_sticker(self._settings.stickers.FAIL)
        await message.answer(text_answer)

    @staticmethod
    async def _answer_on_ok_message(message: types.Message, text_answer: str):
        await message.answer(text_answer)

    def run(self):
        executor.start_polling(self._dispatcher, skip_updates=True)
