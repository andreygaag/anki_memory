from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from anki_bot.forms import DeleteDeckState
from anki_bot.forms import ListDecksForm
from anki_bot.forms import ShowDeckCardState
from anki_bot.models import BotAnkiCard
from anki_bot.user_flows.list_decks import process_list_decks_command
from anki_bot.user_interface import ConfirmationMenu
from anki_bot.user_interface import DeckActionsMenu
from anki_bot.user_interface import ShowCardMenu
from anki_bot.utils import show_card_side
from anki_logic import AnkiApp


class GetCardFromDeckFlow:

    anki: AnkiApp
    show_card_menu = ShowCardMenu()

    def __init__(self, dp: Dispatcher, anki: AnkiApp):
        GetCardFromDeckFlow.anki = anki
        dp.register_message_handler(
            process_get_card_from_deck,
            text=DeckActionsMenu.BTN_SHOW_CARD,
            state=ListDecksForm.wait_deck_action,
        )
        dp.register_message_handler(
            process_get_card_from_deck,
            text=ShowCardMenu.BTN_SHOW_NEXT_RANDOM,
            state=ShowDeckCardState.wait_card_action,
        )
        dp.register_message_handler(
            process_show_side_1_command,
            text=ShowCardMenu.BTN_SHOW_SIDE_1,
            state=ShowDeckCardState.wait_card_action,
        )
        dp.register_message_handler(
            process_show_side_2_command,
            text=ShowCardMenu.BTN_SHOW_SIDE_2,
            state=ShowDeckCardState.wait_card_action,
        )


async def process_get_card_from_deck(message: Message, state: FSMContext):
    async with state.proxy() as data:
        deck_id = data["selected_deck_id"]
    await ShowDeckCardState.wait_card_action.set()
    if card := await GetCardFromDeckFlow.anki.get_random_card_from_deck(deck_id):
        async with state.proxy() as data:
            data["current_card"] = card
        await show_card_side(
            message,
            card.side_1_txt,
            card.side_1_img,
            GetCardFromDeckFlow.show_card_menu.keyboard,
        )
    else:
        await message.answer("Нет карточек")
        await process_list_decks_command(message, state)


async def process_show_side_1_command(message: Message, state: FSMContext):
    async with state.proxy() as data:
        card: BotAnkiCard = data["current_card"]
        await show_card_side(
            message,
            card.side_1_txt,
            card.side_1_img,
            GetCardFromDeckFlow.show_card_menu.keyboard,
        )


async def process_show_side_2_command(message: Message, state: FSMContext):
    async with state.proxy() as data:
        card: BotAnkiCard = data["current_card"]
        await show_card_side(
            message,
            card.side_2_txt,
            card.side_2_img,
            GetCardFromDeckFlow.show_card_menu.keyboard,
        )
