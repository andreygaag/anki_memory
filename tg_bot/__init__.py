import logging
import os

from pyrogram.types import ReplyKeyboardMarkup

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
from pyrogram import Client, filters

bot = Client(
    "anki_memory",
    api_id=int(os.environ["TG_API_ID"]),
    api_hash=os.environ["TG_API_HASH"],
)

state = 0
cached_data = {}
WAIT_SIDE_1 = 1
WAIT_SIDE_2 = 2

@bot.on_message(filters.text & filters.private)
async def echo(client, message):
    await message.reply(message.text)
@bot.on_message(filters.command("start"))
async def process_start_command(client, message):
    async with bot:
        await bot.send_message(
            message.chat.id,
            "Привет!\nЯ - Бот, помогает закрепить знания в памяти методом карточек Anki.\n",
            reply_markup=ReplyKeyboardMarkup(
                [
                    ["Добавить карточку"],
                    ["Случайная карточка"],
                ],
                resize_keyboard=True,
            )
        )

@bot.on_callback_query(filters.regex("add_card"))
async def process_add_card_command(client, callback_query):
    #await AddCardForm.wait_side_1.set()
    state = WAIT_SIDE_1
    await callback_query.answer("Введите первую сторону карточки")

@bot.on_message()
async def process_message(client, message):
    if state == WAIT_SIDE_1:
        cached_data['side_1'] = message.message_id
        state = WAIT_SIDE_2
        await message.answer("Введите вторую сторону карточки")
    elif state == WAIT_SIDE_2:
        cached_data['side_2'] = message.message_id
        # save card in anki layer
        #await anki.create_card(cached_data['side_1'], cached_data['side_2'])
        await message.answer(f"Карточка создана {cached_data['side_1']} {cached_data['side_2']}")
        state = 0
    else:
        await message.reply("Неизвестная команда")

@bot.on_callback_query(filters.regex("random_card"))
async def process_random_card_command(client, callback_query):
    side_1_id, side_2_id = 1,2 # await TelegramBot.anki.random_card()
    async with bot:
        async for message in bot.iter_history("me"):
            if message.message_id == side_1_id:
                await callback_query.answer(message.text)
            if message.message_id == side_2_id:
                await callback_query.answer(message.text)
bot.run()
