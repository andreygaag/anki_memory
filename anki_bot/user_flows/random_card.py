from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from anki_bot.models import BotAnkiCard
from anki_bot.states import ShowRandomCardState
from anki_bot.user_flows.main_menu import process_return_to_main_menu
from anki_bot.user_interface import MainMenu
from anki_bot.user_interface import ShowRandomCardMenu
from anki_bot.utils import show_card_side
from anki_logic import AnkiApp


class RandomCardFlow:

    anki: AnkiApp
    show_card_menu = ShowRandomCardMenu()

    def __init__(self, dp: Dispatcher, anki: AnkiApp):
        RandomCardFlow.anki = anki
        dp.register_message_handler(
            process_random_card_command,
            text=MainMenu.BTN_RANDOM,
        )
        dp.register_message_handler(
            process_random_card_command,
            text=ShowRandomCardMenu.BTN_SHOW_NEXT_RANDOM,
        )
        dp.register_message_handler(
            process_random_card_command,
            text=ShowRandomCardMenu.BTN_SHOW_NEXT_RANDOM,
            state=ShowRandomCardState.wait_card_action,
        )
        dp.register_message_handler(
            process_show_side_1_command,
            text=ShowRandomCardMenu.BTN_SHOW_SIDE_1,
            state=ShowRandomCardState.wait_card_action,
        )
        dp.register_message_handler(
            process_show_side_2_command,
            text=ShowRandomCardMenu.BTN_SHOW_SIDE_2,
            state=ShowRandomCardState.wait_card_action,
        )


async def process_random_card_command(message: Message, state: FSMContext):
    await ShowRandomCardState.wait_card_action.set()
    if card := await RandomCardFlow.anki.get_random_card():
        async with state.proxy() as data:
            data["current_card"] = card
        await show_card_side(
            message,
            card.side_1_txt,
            card.side_1_img,
            RandomCardFlow.show_card_menu.keyboard,
        )
    else:
        await message.answer("Нет карточек")
        await process_return_to_main_menu(message, state)


async def process_show_side_1_command(message: Message, state: FSMContext):
    async with state.proxy() as data:
        card: BotAnkiCard = data["current_card"]
        await show_card_side(
            message,
            card.side_1_txt,
            card.side_1_img,
            RandomCardFlow.show_card_menu.keyboard,
        )


async def process_show_side_2_command(message: Message, state: FSMContext):
    async with state.proxy() as data:
        card: BotAnkiCard = data["current_card"]
        await show_card_side(
            message,
            card.side_2_txt,
            card.side_2_img,
            RandomCardFlow.show_card_menu.keyboard,
        )
