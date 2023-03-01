from aiogram.types import ReplyKeyboardMarkup


class Menu:
    def __init__(self):
        self._keyboard = ReplyKeyboardMarkup()
        self._keyboard.add(*self._get_buttons_text_from_classfields())

    def _get_buttons_text_from_classfields(self):
        return [
            item[1] for item in MainMenu.__dict__.items() if item[0].startswith("BTN_")
        ]

    @property
    def keyboard(self):
        return self._keyboard


class MainMenu(Menu):
    BTN_ADD = "Добавить карточку"
    BTN_RANDOM = "Случайная карточка"
    MENU = "В главное меню"


class ShowSide(Menu):
    BTN_SHOW_SIDE_1 = "Показать сторону 1"
    BTN_SHOW_SIDE_2 = "Показать сторону 2"
    BTN_MAIN_MENU = MainMenu.MENU
