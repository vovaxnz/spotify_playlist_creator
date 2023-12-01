
from typing import List
from aiogram import Bot, types
from chat_utils import PlaylistGenerator, Song
from spotify_utils import SpotifyClient
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import os


TG_BOT_TOKEN=os.getenv("TG_BOT_TOKEN")

playlist_created_message_template = "Playlist created.\nTitle: {title}\nDescription: {description}"

bot = Bot(token=TG_BOT_TOKEN)

dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hello. Write me what playlist do you want")


@dp.message_handler()
async def echo_message(message: types.Message):

    sc = SpotifyClient()

    pg = PlaylistGenerator()

    request_comment = pg.recieve_request(message.text)

    playlist = pg.generate_playlist()

    sc.add_playlist(playlist) 

    response_text = playlist_created_message_template.format(title=playlist.title, description=playlist.description)

    await message.answer(request_comment + "\n\n" + response_text)
    print('Done')


if __name__ == '__main__':
    executor.start_polling(dp)

