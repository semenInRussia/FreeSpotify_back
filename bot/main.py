import logging
import re
from typing import List

from aiogram import Bot, Dispatcher, executor, types

# Configure logging
from entities import Artist, Track
from settings.bot import BOT_TOKEN, BOT_DESCRIPTION, stickers

logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.answer_sticker(stickers.WELCOME)
    await message.answer(BOT_DESCRIPTION)


@dp.message_handler(commands=['top'])
async def get_top(message: types.Message):
    try:
        message_of_answer = _get_detail_artist_message_by_message(message)
    except AttributeError:
        await message.answer("You are inputted not valid band's name.")
    except Exception as e:
        await message.answer_sticker(stickers.FAIL)
        await message.answer("Sorry, I am can't search info about. \n"
                             f"Error: {e.__class__.__name__}. \n")
    else:
        await message.answer(message_of_answer)


def _get_detail_artist_message_by_message(message: types.Message) -> str:
    artist_name = _find_artist_name_in_message(message.text)
    message_of_answer = _get_detail_artist_message_by_name(artist_name)

    return message_of_answer


def _find_artist_name_in_message(message: str):
    result = re.search(r'/top +(.+)', message)
    return result.group(1)


def _get_detail_artist_message_by_name(artist_name) -> str:
    artist = Artist(artist_name)
    message_of_answer = _get_detail_artist_message(artist)

    return message_of_answer


def _get_detail_artist_message(artist: Artist):
    return _get_message_about_artist(artist) + _get_string_top(artist.top)


def _get_message_about_artist(artist: Artist):
    return (
        f"{artist.name}\n"
        f"    IMAGE: {artist.link_on_img}\n"
        f"    LINK: {artist.link}\n"
    )


def _get_string_top(top: List[Track]) -> str:
    string_top = ""

    for i, track in enumerate(top):
        string_top += _get_string_track(track, i)

    return string_top


def _get_string_track(track: Track, index: int) -> str:
    return (
        f"{index + 1}. {track.name} \n"
        f"     ({track.album.name} [{track.album.release_date}])\n"
        f"     {track.album.link}\n"
    )


def run():
    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    run()
