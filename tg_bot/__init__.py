import logging
import os
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from tg_bot import aiogram_monkey
from tg_bot.keyboards import InlineKeyboards

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

bot = Bot(os.getenv("TELEGRAM_BOT_TOKEN"))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class AddCardForm(StatesGroup):
    wait_side_1 = State()
    wait_side_2 = State()




class TelegramBot:

    anki = None

    @classmethod
    async def create(cls, anki):
        self = TelegramBot()
        TelegramBot.anki = anki

        # monkey patch
        executor.Executor = aiogram_monkey.MyExecutor
        executor.start_polling = aiogram_monkey.start_polling

        TelegramBot.keyboards = InlineKeyboards()
        await executor.start_polling(dp, skip_updates=True)

        logging.info("Initializing TelegramBot")
        return self

    @dp.message_handler(commands=['start'], state="*")
    async def process_start_command(message: types.Message):
        await message.reply(
            "Привет!\nЯ - Бот, помогает закрепить знания в памяти методом карточек Anki.\n",
            reply_markup=TelegramBot.keyboards.main_menu,
        )

    @dp.callback_query_handler(text="add_card")
    @dp.message_handler(commands=['add_card'], state="*")
    async def process_add_card_command(message: types.Message | types.CallbackQuery):
        chat_id = message.chat.id if type(message) == types.Message else message.message.chat.id
        await AddCardForm.wait_side_1.set()
        await bot.send_message(chat_id, "Введите первую сторону карточки")


    @dp.message_handler(state=AddCardForm.wait_side_1)
    async def process_side_1(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['side_1'] = message.message_id
            await AddCardForm.next()
            await message.answer("Введите вторую сторону карточки")

    @dp.message_handler(state=AddCardForm.wait_side_2)
    async def process_side_2(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['side_2'] = message.message_id
        # save card in anki layer
        await TelegramBot.anki.create_card(data['side_1'], data['side_2'])
        await message.answer(f"Карточка создана {data['side_1']} {data['side_2']} {TelegramBot.anki}")
        await state.finish()

    @dp.callback_query_handler(text="random_card")
    @dp.message_handler(commands=['random_card'])
    async def process_random_card_command(message: types.Message):
        side_1_id, side_2_id = await TelegramBot.anki.random_card()

        chat_id = message.chat.id if type(message) == types.Message else message.message.chat.id
        chat = await bot.get_chat(chat_id)
        await bot.send_message(chat_id, f"Сторона 1:")
        await bot.forward_message(chat_id=chat_id, from_chat_id=chat_id, message_id=side_1_id)
        await bot.send_message(chat_id, f"Сторона 2:")
        await bot.forward_message(chat_id=chat_id, from_chat_id=chat_id, message_id=side_2_id,)

        await message.answer(f"Карточка {card}")
        await bot

    # @dp.message_handler()
    async def echo_message(msg: types.Message):
        await msg.answer(msg.text)
