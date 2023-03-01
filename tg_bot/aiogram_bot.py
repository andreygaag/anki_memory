import logging
import os

from aiogram import Bot
from aiogram import Dispatcher
from aiogram import executor
from aiogram import types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentTypes

from anki import AnkiMemApp
from tg_bot import aiogram_monkey
from tg_bot.forms import AddCardForm
from tg_bot.forms import ShowCardForm
from tg_bot.ui import MainMenu
from tg_bot.ui import Menu
from tg_bot.ui import ShowCardMenu

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

bot = Bot(os.getenv("TELEGRAM_BOT_TOKEN"))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class AnkiMemBot:

    anki: AnkiMemApp
    main_menu: Menu = MainMenu()
    show_card_menu: Menu = ShowCardMenu()

    @classmethod
    async def create(cls, anki):
        self = AnkiMemBot()
        AnkiMemBot.anki = anki

        # monkey patch
        executor.Executor = aiogram_monkey.MyExecutor
        executor.start_polling = aiogram_monkey.start_polling

        await executor.start_polling(dp, skip_updates=True)

        logging.info("Initializing TelegramBot")
        return self


""" Main menu """


@dp.message_handler(commands=["start"], state="*")
async def process_start_command(message: types.Message):
    await message.reply(
        "Привет!\nЯ - Бот, помогает закрепить знания в памяти методом карточек Anki.\n",
        reply_markup=AnkiMemBot.main_menu.keyboard,
    )


@dp.message_handler(text=MainMenu.MENU)
async def return_to_main_menu(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(
        "Выберите действие",
        reply_markup=AnkiMemBot.main_menu.keyboard,
    )


""" Add card flow """


@dp.message_handler(text=MainMenu.BTN_ADD)
async def process_add_card_command(message: types.Message):
    await AddCardForm.wait_side_1.set()
    await message.answer("Введите первую сторону карточки")


@dp.message_handler(
    state=AddCardForm.wait_side_1,
    content_types=ContentTypes.TEXT | ContentTypes.PHOTO,
)
async def process_side_1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["side_1"] = message.message_id
        await AddCardForm.next()
        await message.answer("Введите вторую сторону карточки")


@dp.message_handler(
    state=AddCardForm.wait_side_2,
    content_types=ContentTypes.TEXT | ContentTypes.PHOTO,
)
async def process_side_2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["side_2"] = message.message_id
        await AnkiMemBot.anki.create_card(data["side_1"], data["side_2"])
        await message.answer(
            f"Карточка создана {data['side_1']} {data['side_2']} {AnkiMemBot.anki}",
        )
    await state.finish()


""" Show random card flow """


@dp.message_handler(text=MainMenu.BTN_RANDOM)
@dp.message_handler(text=ShowCardMenu.BTN_SHOW_NEXT_RANDOM)
async def process_random_card_command(message: types.Message, state: FSMContext):
    ShowCardForm.show_card.set()
    side_1_id, side_2_id = await AnkiMemBot.anki.random_card()
    async with state.proxy() as data:
        data["side_1_id"] = side_1_id
        data["side_2_id"] = side_2_id
    await message.answer(
        f"Что показать?",
        reply_markup=AnkiMemBot.show_card_menu.keyboard,
    )


@dp.message_handler(text=ShowCardMenu.BTN_SHOW_SIDE_1)
async def process_show_side_1_command(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await bot.forward_message(message.chat.id, message.chat.id, data["side_1_id"])


@dp.message_handler(text=ShowCardMenu.BTN_SHOW_SIDE_2)
async def process_show_side_2_command(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await bot.forward_message(message.chat.id, message.chat.id, data["side_2_id"])


# TODO card list with management menu
