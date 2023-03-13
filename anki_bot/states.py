from aiogram.dispatcher.filters.state import State
from aiogram.dispatcher.filters.state import StatesGroup


class CreateCardState(StatesGroup):
    wait_side_1 = State()
    wait_side_2 = State()
    wait_deck_selection = State()


class ShowRandomCardState(StatesGroup):
    wait_card_action = State()


class ShowNextCardState(StatesGroup):
    wait_card_action = State()


class DeleteCardState(StatesGroup):
    wait_confirmation = State()


class CreateDeckForm(StatesGroup):
    wait_deck_name = State()


class ListDecksState(StatesGroup):
    list_decks = State()
    wait_deck_action = State()


class DeleteDeckState(StatesGroup):
    wait_confirmation = State()


class ShowDeckCardState(StatesGroup):
    wait_card_action = State()
