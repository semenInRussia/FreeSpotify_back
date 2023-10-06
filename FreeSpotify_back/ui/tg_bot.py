import asyncio
import logging
import traceback

from aiogram import Bot, Dispatcher, filters, types
from FreeSpotify_back._low_level_utils import format_exception
from FreeSpotify_back.settings.bot import bot
from loguru import logger

from .ui import AbstractUI

logging.basicConfig(level=logging.INFO)

_default_settings = bot


def _create_telegram_settings(additional_settings=None):  # noqa: ANN202, ANN001
    return _default_settings + additional_settings


class TelegramUI(AbstractUI):
    """The class runner for `FreeSpotify_back` telegram bot."""

    _parse_mode_name = "markdown"

    def __init__(
        self,
        additional_telegram_settings=None,  # noqa: ANN001
        additional_entities_settings=None,
    ):  # noqa: ANN001
        """Build a new `FreeSpotify_back` telegram bot runner with given settings."""
        self._telegram_settings = _create_telegram_settings(
            additional_telegram_settings
        )
        super().__init__(additional_entities_settings)

    async def run(self) -> None:
        bot_ = Bot(token=self._telegram_settings.BOT_TOKEN)

        dp = Dispatcher()

        @dp.message(filters.Command("help"))
        @dp.message(filters.CommandStart())
        async def get_bot_help_information(message: types.Message) -> None:
            """Send to the user helpful message."""
            await message.answer(self._telegram_settings.BOT_DESCRIPTION)
            await message.answer_sticker(self._telegram_settings.stickers.WELCOME)

        @dp.message()
        async def handle_tg_message(message: types.Message):  # noqa: ANN202
            if message.text is None:
                await self.print_normal_message(
                    "You sent a thing without text", message
                )
                return
            try:
                self.handle_user_message(message.text, message)
            except Exception as err:  # noqa: BLE001
                await self.print_error(err, message)
                print(traceback.format_exc())

        await dp.start_polling(bot_)

    async def print_normal_message(
        self, message: str, aiogram_message: types.Message
    ) -> None:
        logger.info("Print normal message")
        await aiogram_message.answer(message, parse_mode="markdown")

    async def print_error(
        self, error: Exception, aiogram_message: types.Message
    ) -> None:
        logger.warning(f"Error: {error.__class__.__name__}")

        await aiogram_message.answer_sticker(self._telegram_settings.stickers.FAIL)
        await aiogram_message.answer(format_exception(error))


if __name__ == "__main__":
    ui = TelegramUI()
    asyncio.run(ui.run())
