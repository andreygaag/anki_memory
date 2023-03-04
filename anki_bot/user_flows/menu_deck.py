from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from anki_bot.user_interface import DecksMenu
from anki_bot.user_interface import MainMenu


class MenuDeckFlow:

    decks_menu = DecksMenu()

    def __init__(self, dp: Dispatcher):
        dp.register_message_handler(
            process_deck_menu_command,
            text=MainMenu.BTN_DECKS,
        )


async def process_deck_menu_command(message: Message, state: FSMContext):
    await state.finish()
    await message.answer(
        "Выберите действие",
        reply_markup=MenuDeckFlow.decks_menu.keyboard,
    )
