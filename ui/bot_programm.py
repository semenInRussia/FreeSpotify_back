import logging

from aiogram import Bot
from aiogram import Dispatcher
from aiogram import types
from aiogram.utils import executor

from _low_level_utils import format_exception
from settings.bot import bot
from ui.abstract_ui import AbstractUI
from ui.handler_collection import AsyncHandlersCollection

logging.basicConfig(level=logging.INFO)

_default_settings = bot

handlers_telegram = AsyncHandlersCollection()


@handlers_telegram.new_handler("print normal message")
async def print_normal_message(message: str, aiogram_message: types.Message, *args):
    await aiogram_message.answer(message, parse_mode="markdown")


@handlers_telegram.new_handler("print error")
async def print_error(
        error: Exception,
        aiogram_message: types.Message,
        settings
):
    await aiogram_message.answer_sticker(settings.stickers.FAIL)
    await aiogram_message.answer(format_exception(error))


def _create_telegram_settings(additional_settings=None):
    return _default_settings + additional_settings


class TelegramUI(AbstractUI):
    handlers: AsyncHandlersCollection
    _parse_mode_name = "markdown"

    def __init__(self, additional_telegram_settings=None, additional_entities_settings=None):
        self._telegram_settings = _create_telegram_settings(additional_telegram_settings)
        self.handlers = handlers_telegram

        super().__init__(additional_entities_settings)

    def run(self):
        bot_ = Bot(token=self._telegram_settings.BOT_TOKEN)

        dispatcher = Dispatcher(bot_)

        @dispatcher.message_handler(commands=["help"])
        async def get_bot_help_information(message: types.Message):
            await message.answer(self._telegram_settings.BOT_DESCRIPTION)
            await message.answer_sticker(self._telegram_settings.stickers.WELCOME)

        @dispatcher.message_handler()
        async def get_top(message: types.Message):
            artist_name = message.text

            self.print_artist(artist_name)

            await self.handlers.execute_calls_queue(
                message,
                self._telegram_settings
            )

        executor.start_polling(dispatcher, skip_updates=True)


if __name__ == "__main__":
    telegram_ui = TelegramUI()

    telegram_ui.run()
