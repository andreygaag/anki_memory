from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from anki_bot.user_interface import MainMenu


class MainMenuFlow:

    main_menu = MainMenu()

    def __init__(self, dp: Dispatcher):
        dp.register_message_handler(
            process_start_command,
            commands=["start"],
            state="*",
        )
        dp.register_message_handler(
            process_return_to_main_menu,
            text=MainMenu.BTN_MENU,
            state="*",
        )


async def process_start_command(message: Message, state: FSMContext):
    await state.finish()
    await message.reply(
        "Привет!\nЯ - Бот, помогает закрепить знания в памяти методом карточек Anki.\n",
        reply_markup=MainMenuFlow.main_menu.keyboard,
    )


async def process_return_to_main_menu(message: Message, state: FSMContext):
    await state.finish()
    await message.answer(
        "Выберите действие",
        reply_markup=MainMenuFlow.main_menu.keyboard,
    )
