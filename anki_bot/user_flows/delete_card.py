import types

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from anki_bot.models import BotAnkiCard
from anki_bot.states import DeleteCardState
from anki_bot.states import ShowDeckCardState
from anki_bot.states import ShowNextCardState
from anki_bot.states import ShowRandomCardState
from anki_bot.user_flows.main_menu import process_return_to_main_menu
from anki_bot.user_interface import ConfirmationMenu
from anki_bot.user_interface import ShowNextCardMenu
from anki_bot.user_interface import ShowRandomCardMenu
from anki_bot.user_interface import ShowRandomDeckCardMenu
from anki_logic import AnkiApp


class DeleteCardFlow:

    anki: AnkiApp

    def __init__(self, dp: Dispatcher, anki: AnkiApp):
        DeleteCardFlow.anki = anki
        dp.register_message_handler(
            process_delete_card_command,
            text=ShowRandomCardMenu.BTN_DELETE,
            state=ShowRandomCardState.wait_card_action,
        )
        dp.register_message_handler(
            process_delete_card_command,
            text=ShowRandomDeckCardMenu.BTN_DELETE,
            state=ShowDeckCardState.wait_card_action,
        )
        dp.register_message_handler(
            process_delete_card_command,
            text=ShowNextCardMenu.BTN_DELETE,
            state=ShowNextCardState.wait_card_action,
        )
        dp.register_message_handler(
            process_delete_card_confirmation,
            state=DeleteCardState.wait_confirmation,
        )


async def process_delete_card_command(message: Message, state: FSMContext):
    async with state.proxy() as data:
        card: BotAnkiCard = data["current_card"]
    await DeleteCardState.wait_confirmation.set()
    await message.answer("Точно удалить?", reply_markup=ConfirmationMenu().keyboard)
    async with state.proxy() as data:
        data["current_card"] = card


async def process_delete_card_confirmation(message: Message, state: FSMContext):
    async with state.proxy() as data:
        card: BotAnkiCard = data["current_card"]
    if message.text == ConfirmationMenu.BTN_YES:
        await DeleteCardFlow.anki.delete_card(card.card_id)
        await message.answer("Карточка удалена")
        await process_return_to_main_menu(message, state)
    elif message.text == ConfirmationMenu.BTN_NO:
        await message.answer("Удаление отменено")
        await process_return_to_main_menu(message, state)
    else:
        await message.answer("Да или нет?")
