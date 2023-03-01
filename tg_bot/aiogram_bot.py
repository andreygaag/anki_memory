import logging
import os
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentTypes

from tg_bot import aiogram_monkey
from tg_bot.forms import AddCardForm
from tg_bot.ui import MainMenu

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

bot = Bot(os.getenv("TELEGRAM_BOT_TOKEN"))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class Bot:

    anki = None
    main_menu = MainMenu()

    @classmethod
    async def create(cls, anki):
        self = Bot()
        Bot.anki = anki

        # monkey patch
        executor.Executor = aiogram_monkey.MyExecutor
        executor.start_polling = aiogram_monkey.start_polling

        await executor.start_polling(dp, skip_updates=True)

        logging.info("Initializing TelegramBot")
        return self

""" Message handlers """
@dp.message_handler(commands=['start'], state="*")
async def process_start_command(message: types.Message):
    await message.reply(
        "Привет!\nЯ - Бот, помогает закрепить знания в памяти методом карточек Anki.\n",
        reply_markup=Bot.main_menu.keyboard,
    )

@dp.message_handler(state=AddCardForm.wait_side_1, content_types=ContentTypes.TEXT | ContentTypes.PHOTO)
async def process_side_1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['side_1'] = message.message_id
        await AddCardForm.next()
        await message.answer("Введите вторую сторону карточки")

@dp.message_handler(state=AddCardForm.wait_side_2, content_types=ContentTypes.TEXT | ContentTypes.PHOTO)
async def process_side_2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['side_2'] = message.message_id
    await Bot.anki.create_card(data['side_1'], data['side_2'])
    await message.answer(f"Карточка создана {data['side_1']} {data['side_2']} {Bot.anki}")
    await state.finish()

@dp.message_handler(text=MainMenu.BTN_RANDOM)
async def process_random_card_command(message: types.Message):
    side_1_id, side_2_id = await Bot.anki.random_card()

    chat_id = message.chat.id if type(message) == types.Message else message.message.chat.id
    await message.answer(f"Сторона 1:")
    await bot.forward_message(chat_id=chat_id, from_chat_id=chat_id, message_id=side_1_id)
    await message.answer(f"Сторона 2:")
    await bot.forward_message(chat_id=chat_id, from_chat_id=chat_id, message_id=side_2_id,)

@dp.message_handler(text=MainMenu.BTN_ADD)
async def process_add_card_command(message: types.Message):
    await AddCardForm.wait_side_1.set()
    await message.answer("Введите первую сторону карточки")

