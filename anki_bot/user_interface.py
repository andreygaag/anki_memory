import abc

from aiogram.types import InlineKeyboardButton
from aiogram.types import KeyboardButton
from aiogram.types import ReplyKeyboardMarkup


class ReplyMarkup:
    def __init__(self):
        self._keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    @property
    def keyboard(self):
        return self._keyboard


class Keyboard(ReplyMarkup):
    def __init__(self):
        self._keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        self._keyboard.add(
            *[
                KeyboardButton(btn_text)
                for btn_text in self._get_buttons_text_from_classfields()
            ]
        )

    def _get_buttons_text_from_classfields(self):
        return [
            item[1]
            for item in self.__class__.__dict__.items()
            if item[0].startswith("BTN_")
        ]


class MainMenu(Keyboard):
    BTN_CREATE = "Создать карточку"
    BTN_RANDOM = "Случайная карточка"
    BTN_DECKS = "Управление колодами"
    BTN_MENU = "В главное меню"

    def __init__(self):
        super().__init__()


""" Decks """


class DecksMenu(Keyboard):
    BTN_CREATE = "Создать колоду"
    BTN_LIST = "Список колод"
    BTN_MENU = MainMenu.BTN_MENU

    def __init__(self):
        super().__init__()


class ListDecksMenu(ReplyMarkup):
    def __init__(self, decks: list[str]):
        super().__init__()
        self._keyboard.add(*[InlineKeyboardButton(deck) for deck in decks])
        self.keyboard.add(MainMenu.BTN_MENU)


class DeckActionsMenu(Keyboard):
    BTN_DELETE = "Удалить колоду"
    BTN_MENU = MainMenu.BTN_MENU

    def __init__(self):
        super().__init__()


class ConfirmationMenu(Keyboard):
    BTN_YES = "Да"
    BTN_NO = "Нет"
    BTN_MENU = MainMenu.BTN_MENU

    def __init__(self):
        super().__init__()


""" Cards """


class ShowCardMenu(Keyboard):
    BTN_SHOW_SIDE_1 = "Показать сторону 1"
    BTN_SHOW_SIDE_2 = "Показать сторону 2"
    BTN_SHOW_NEXT_RANDOM = "Следующая случайная карточка"
    BTN_DELETE = "Удалить карточку"
    BTN_MENU = MainMenu.BTN_MENU

    def __init__(self):
        super().__init__()
