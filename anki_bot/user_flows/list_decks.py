from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from anki_bot.states import ListDecksState
from anki_bot.user_flows.menu_deck import process_deck_menu_command
from anki_bot.user_interface import DecksMenu
from anki_bot.user_interface import ListDecksMenu
from anki_logic import AnkiApp


class ListDecksFlow:

    anki: AnkiApp

    def __init__(self, dp: Dispatcher, anki: AnkiApp):
        ListDecksFlow.anki = anki
        dp.register_message_handler(
            process_list_decks_command,
            text=DecksMenu.BTN_LIST,
        )


async def process_list_decks_command(message: Message, state: FSMContext):
    if decks_names := await ListDecksFlow.anki.list_decks_names():
        await ListDecksState.list_decks.set()
        await message.answer(
            "Выберите колоду",
            reply_markup=ListDecksMenu(decks_names).keyboard,
        )
    else:
        await state.finish()
        await message.answer("У вас нет колод")
        await process_deck_menu_command(message, state)
