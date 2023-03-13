import types

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from anki_bot.states import CreateDeckForm
from anki_bot.user_interface import DecksMenu
from anki_logic import AnkiApp


class CreateDeckFlow:

    anki: AnkiApp

    def __init__(self, dp: Dispatcher, anki: AnkiApp):
        CreateDeckFlow.anki = anki
        dp.register_message_handler(
            process_create_deck_command,
            text=DecksMenu.BTN_CREATE,
        )
        dp.register_message_handler(
            process_deck_name,
            state=CreateDeckForm.wait_deck_name,
        )


async def process_create_deck_command(message: Message):
    await CreateDeckForm.wait_deck_name.set()
    await message.answer("Введите название колоды")


async def process_deck_name(message: Message, state: FSMContext):
    deck_name = message.text
    await CreateDeckFlow.anki.create_deck(deck_name)
    await message.answer(f"Колода {deck_name} создана")
    await state.finish()
