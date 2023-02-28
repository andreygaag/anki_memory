from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class InlineKeyboards:

    def __init__(self):
        self._main_menu = InlineKeyboardMarkup(
            row_width=1
        )
        self._main_menu.add(
            InlineKeyboardButton("Добавить карточку", callback_data="add_card"),
            InlineKeyboardButton("Случайная карточка", callback_data="random_card"),
        )

    @property
    def main_menu(self):
        return self._main_menu