from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


class Menu:
    def __init__(self):
        self._keyboard = ReplyKeyboardMarkup()
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

    @property
    def keyboard(self):
        return self._keyboard


class MainMenu(Menu):
    BTN_ADD = "Добавить карточку!"
    BTN_RANDOM = "Случайная карточка!"
    MENU = "В главное меню"

    def __init__(self):
        super().__init__()


class ShowCardMenu(Menu):
    BTN_SHOW_SIDE_1 = "Показать сторону 1"
    BTN_SHOW_SIDE_2 = "Показать сторону 2"
    BTN_SHOW_NEXT_RANDOM = "Следующая случайная карточка"
    BTN_MAIN_MENU = MainMenu.MENU

    def __init__(self):
        super().__init__()
