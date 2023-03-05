import os

import aiofiles
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from anki_bot.forms import ShowCardForm
from anki_bot.models import BotAnkiCard
from anki_bot.user_flows.main_menu import process_return_to_main_menu
from anki_bot.user_interface import MainMenu
from anki_bot.user_interface import ShowCardMenu
from anki_bot.utils import build_media_path
from anki_bot.utils import download_message_photo_by_message_id
from anki_logic import AnkiApp


class RandomCardFlow:

    anki: AnkiApp
    show_card_menu = ShowCardMenu()

    def __init__(self, dp: Dispatcher, anki: AnkiApp):
        RandomCardFlow.anki = anki
        dp.register_message_handler(
            process_random_card_command,
            text=MainMenu.BTN_RANDOM,
        )
        dp.register_message_handler(
            process_random_card_command,
            text=ShowCardMenu.BTN_SHOW_NEXT_RANDOM,
        )
        dp.register_message_handler(
            process_random_card_command,
            text=ShowCardMenu.BTN_SHOW_NEXT_RANDOM,
            state=ShowCardForm.wait_card_action,
        )
        dp.register_message_handler(
            process_show_side_1_command,
            text=ShowCardMenu.BTN_SHOW_SIDE_1,
            state=ShowCardForm.wait_card_action,
        )
        dp.register_message_handler(
            process_show_side_2_command,
            text=ShowCardMenu.BTN_SHOW_SIDE_2,
            state=ShowCardForm.wait_card_action,
        )


async def show_card_side(message: Message, card_txt, card_img, state: FSMContext):
    if card_img:
        # Скачать
        await download_message_photo_by_message_id(message.bot, card_img)
        async with aiofiles.open(build_media_path(card_img), "rb") as file:
            # Отправить
            await message.answer_photo(
                caption=card_txt,
                photo=await file.read(),
                reply_markup=RandomCardFlow.show_card_menu.keyboard,
            )
        # Удалить
        os.remove(build_media_path(card_img))
    else:
        await message.answer(
            text=card_txt,
            reply_markup=RandomCardFlow.show_card_menu.keyboard,
        )


async def process_random_card_command(message: Message, state: FSMContext):
    # TODO: refactoring - extract show message function
    await ShowCardForm.wait_card_action.set()
    if card := await RandomCardFlow.anki.get_random_card():
        async with state.proxy() as data:
            data["current_card"] = card
        await show_card_side(message, card.side_1_txt, card.side_1_img, state)
    else:
        await message.answer("Нет карточек")
        await process_return_to_main_menu(message, state)


async def process_show_side_1_command(message: Message, state: FSMContext):
    async with state.proxy() as data:
        card: BotAnkiCard = data["current_card"]
        await show_card_side(message, card.side_1_txt, card.side_1_img, state)


async def process_show_side_2_command(message: Message, state: FSMContext):
    async with state.proxy() as data:
        card: BotAnkiCard = data["current_card"]
        await show_card_side(message, card.side_2_txt, card.side_2_img, state)
