from aiogram.types import ReplyKeyboardMarkup


class MainMenu:
    BTN_ADD = "Добавить карточку",
    BTN_RANDOM = "Случайная карточка",
    def __init__(self):
        self._keyboard = ReplyKeyboardMarkup()
        self._keyboard.add(*self._get_buttons_text_from_classfields())
    def _get_buttons_text_from_classfields(self):
        return [item[1][0] for item in MainMenu.__dict__.items() if item[0].startswith("BTN_")]
    @property
    def keyboard(self):
        return self._keyboard