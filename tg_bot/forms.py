from aiogram.dispatcher.filters.state import State
from aiogram.dispatcher.filters.state import StatesGroup


class AddCardForm(StatesGroup):
    wait_side_1 = State()
    wait_side_2 = State()


class ShowCardForm(StatesGroup):
    show_card = State()
