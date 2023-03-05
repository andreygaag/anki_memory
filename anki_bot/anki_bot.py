import logging
import os

from aiogram import Bot
from aiogram import Dispatcher
from aiogram import executor
from aiogram import types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.middlewares import BaseMiddleware

from anki_bot import aiogram_monkey
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

        # Monkey patch for run in current event loop
        executor.Executor = aiogram_monkey.MyExecutor
        executor.start_polling = aiogram_monkey.start_polling

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
        await executor.start_polling(dp, skip_updates=True)
        logging.info("Initializing TelegramBot")
        return self
