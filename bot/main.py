import logging
from typing import List

from aiogram import Bot, Dispatcher, executor, types

# Configure logging
from entities import Artist, Track
from settings.bot import BOT_TOKEN, BOT_DESCRIPTION

logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply(BOT_DESCRIPTION)


def _get_string_track(track: Track, index: int) -> str:
    return (
        f"{index + 1}. {track.name} \n"
        f"     ({track.album.name} [{track.album.release_date}])\n"
        f"     {track.album.link}\n"
    )


def _get_string_top(top: List[Track]) -> str:
    return "\n".join(
        [
            _get_string_track(track, i) for i, track in enumerate(top)
        ]
    )


def _get_message_about_artist(artist: Artist):
    return (
        f"{artist.name}\n"
        f"    IMAGE: {artist.link_on_img}\n"
        f"    LINK: {artist.link}\n"
    )


def _get_detail_artist_message(artist: Artist):
    return _get_message_about_artist(artist) + _get_string_top(artist.top)


@dp.message_handler()
async def get_top(message: types.Message):
    artist = Artist(message.text)

    message_of_answer = _get_detail_artist_message(artist)

    await message.answer(message_of_answer)


def run():
    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    run()
