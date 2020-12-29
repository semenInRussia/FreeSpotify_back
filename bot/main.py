import logging
import re
from typing import List

from aiogram import Bot, Dispatcher, executor, types
# Configure logging
from loguru import logger

from bot.core.exceptions import NotInputtedSearch
from entities import Artist, Track
from music_manger.core.exceptions import NotFoundAlbumException, NotFoundTrackException
from settings.bot import BOT_TOKEN, BOT_DESCRIPTION, stickers

logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.answer_sticker(stickers.WELCOME)
    await message.answer(BOT_DESCRIPTION)


def _parse_search_string(search_string: str) -> tuple:
    """
    Parse searching string. Example:
    "ac dc - back in black" -> ("ac dc", "back in black")
    :param search_string: Example: "ac dc - back in black"
    :return: artist name, track name
    """
    res = re.search(r"\s*(?P<artist_name>.+)\s*-\s*(?P<track_name>.+)\s*", search_string)

    return res.group('artist_name'), res.group('track_name')


def _get_track_by_message(message_text: str) -> Track:
    search_string = _find_arguments_of_command_message(message_text)

    artist_name, track_name = _parse_search_string(search_string)
    album_name = ""

    return Track(artist_name, album_name, track_name)


def _get_detail_track_by_message(message_text: str) -> str:
    track = _get_track_by_message(message_text)

    return _get_string_detail_track(track)


def _get_string_detail_track(track: Track) -> str:
    return (
        f"{track.name} \n"
        f"     {track.album.name} [{track.album.release_date}]\n"
        f"     {track.album.link}\n"
    )


@dp.message_handler(commands=['search'])
async def search_track(message: types.Message):
    try:
        answer_message = _get_detail_track_by_message(message.text)
    except NotInputtedSearch as e:
        await message.answer("You don't enter search")
        logger.debug(e)
    except NotFoundAlbumException:
        await message.answer("I'm don't found album")
        await message.answer_sticker(stickers.FAIL)
    except NotFoundTrackException:
        await message.answer("I'm don't found album")
        await message.answer_sticker(stickers.FAIL)
    else:
        await message.answer(answer_message)


def _find_arguments_of_command_message(message: str):
    result = re.search(r'/(?P<command_name>\w+)\s+(?P<argument>.+)', message)

    try:
        return result.group('argument')
    except AttributeError:
        raise NotInputtedSearch


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
    artist_name = _find_arguments_of_command_message(message.text)

    message_of_answer = _get_detail_artist_message_by_name(artist_name)

    return message_of_answer


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
        string_top += _get_string_top_item(track, i)

    return string_top


def _get_string_top_item(track: Track, index: int) -> str:
    string_track = _get_string_detail_track(track)
    top_number = index + 1

    return f"{top_number}. {string_track}"


def run():
    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    run()
