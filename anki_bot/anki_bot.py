import logging
import os

from aiogram import Bot
from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from anki_bot.executor import start_polling_in_current_loop
from anki_bot.middlewares import OnlyCreatorCanLaunchMiddleware
from anki_bot.middlewares import StateLoggingMiddleware
from anki_bot.user_flows.create_card import CreateCardFlow
from anki_bot.user_flows.create_deck import CreateDeckFlow
from anki_bot.user_flows.delete_card import DeleteCardFlow
from anki_bot.user_flows.delete_deck import DeleteDeckFlow
from anki_bot.user_flows.get_deck import GetDeckFlow
from anki_bot.user_flows.list_decks import ListDecksFlow
from anki_bot.user_flows.main_menu import MainMenuFlow
from anki_bot.user_flows.menu_deck import MenuDeckFlow
from anki_bot.user_flows.random_card import RandomCardFlow

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

bot = Bot(os.getenv("TELEGRAM_BOT_TOKEN"))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(StateLoggingMiddleware())
dp.middleware.setup(OnlyCreatorCanLaunchMiddleware())


class AnkiBot:
    @classmethod
    async def create(cls, anki):
        self = cls()

        # Register handlers
        MainMenuFlow(dp)
        MenuDeckFlow(dp)
        ListDecksFlow(dp, anki)
        GetDeckFlow(dp, anki)
        DeleteDeckFlow(dp, anki)
        CreateDeckFlow(dp, anki)
        CreateCardFlow(dp, anki)
        RandomCardFlow(dp, anki)
        DeleteCardFlow(dp, anki)

        # Run handlers
        await start_polling_in_current_loop(dp, skip_updates=True)
        logging.info("Initializing TelegramBot")
        return self
