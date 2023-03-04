from aiogram.dispatcher.filters.state import State
from aiogram.dispatcher.filters.state import StatesGroup


class CreateCardForm(StatesGroup):
    wait_side_1 = State()
    wait_side_2 = State()
    wait_deck_selection = State()


class ShowCardForm(StatesGroup):
    wait_card_action = State()


class DeleteCardForm(StatesGroup):
    wait_confirmation = State()


class CreateDeckForm(StatesGroup):
    wait_deck_name = State()


class ListDecksForm(StatesGroup):
    list_decks = State()
    wait_deck_action = State()


class DeleteDeckState(StatesGroup):
    wait_confirmation = State()
