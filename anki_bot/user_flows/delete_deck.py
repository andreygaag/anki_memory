from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from anki_bot.states import DeleteDeckState
from anki_bot.states import ListDecksState
from anki_bot.user_flows.list_decks import process_list_decks_command
from anki_bot.user_interface import ConfirmationMenu
from anki_bot.user_interface import DeckActionsMenu
from anki_logic import AnkiApp


class DeleteDeckFlow:

    anki: AnkiApp
    delete_confirmation_menu = ConfirmationMenu()

    def __init__(self, dp: Dispatcher, anki: AnkiApp):
        DeleteDeckFlow.anki = anki
        dp.register_message_handler(
            process_delete_deck_command,
            state=ListDecksState.wait_deck_action,
            text=DeckActionsMenu.BTN_DELETE,
        )
        dp.register_message_handler(
            process_delete_deck_confirmation,
            state=DeleteDeckState.wait_confirmation,
        )


async def process_delete_deck_command(message: Message, state: FSMContext):
    async with state.proxy() as data:
        deck_id = data["selected_deck_id"]
    await DeleteDeckState.wait_confirmation.set()
    async with state.proxy() as data:
        data["selected_deck_id"] = deck_id
    await message.answer(
        f"Вы уверены, что хотите удалить колоду {message.text}?",
        reply_markup=DeleteDeckFlow.delete_confirmation_menu.keyboard,
    )


async def process_delete_deck_confirmation(message: Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == ConfirmationMenu.BTN_YES:
            await DeleteDeckFlow.anki.delete_deck(data["selected_deck_id"])
            await message.answer(f"Колода удалена")
            await state.finish()
            await process_list_decks_command(message, state)
        elif message.text == ConfirmationMenu.BTN_NO:
            await state.finish()
            await message.answer(f"На нет и суда нет.")
            await process_list_decks_command(message, state)
        else:
            await message.answer(f"Да или нет?")
