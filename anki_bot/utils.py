import os

import aiofiles
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


async def show_card_side(message: Message, card_txt, card_img, reply_markup):
    if card_img:
        # Скачать
        await download_message_photo_by_message_id(message.bot, card_img)
        async with aiofiles.open(build_media_path(card_img), "rb") as file:
            # Отправить
            await message.answer_photo(
                caption=card_txt,
                photo=await file.read(),
                reply_markup=reply_markup,
            )
        # Удалить
        os.remove(build_media_path(card_img))
    else:
        await message.answer(
            text=card_txt,
            reply_markup=reply_markup,
        )
