import types

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from anki_bot.states import ListDecksState
from anki_bot.user_interface import DeckActionsMenu
from anki_bot.user_interface import DecksMenu
from anki_logic import AnkiApp


class GetDeckFlow:

    anki: AnkiApp
    deck_actions_menu = DeckActionsMenu()

    def __init__(self, dp: Dispatcher, anki: AnkiApp):
        GetDeckFlow.anki = anki
        dp.register_message_handler(
            process_deck_name,
            state=ListDecksState.list_decks,
        )


async def process_deck_name(message: Message, state: FSMContext):
    async with state.proxy() as data:
        if deck_id := await GetDeckFlow.anki.get_deck_id_by_name(message.text):
            data["selected_deck_id"] = deck_id
            await ListDecksState.wait_deck_action.set()
            await message.answer(
                f"Выбрана колода {message.text}",
                reply_markup=GetDeckFlow.deck_actions_menu.keyboard,
            )
        else:
            await message.answer("Такой колоды нет")
            return
