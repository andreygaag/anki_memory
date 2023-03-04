import os

from aiogram import Bot
from aiogram.types import Message


def build_media_path(filename: str | int) -> str:
    return os.path.join(
        os.getcwd(),
        os.getenv("MEDIA_DIR", ""),
        f"{filename}.jpg",
    )


async def download_message_photo_by_message_id(bot: Bot, telegram_file_id: int) -> str:
    file_path = build_media_path(telegram_file_id)
    await bot.download_file_by_id(telegram_file_id, file_path)
    return file_path


async def check_and_download_message_photo(message: Message) -> str | None:
    # TODO: Drop long files and check storege
    if message.photo:
        telegram_file_id = message.photo.pop().file_unique_id
        await download_message_photo_by_message_id(message.bot, telegram_file_id)
        return telegram_file_id
    return None
