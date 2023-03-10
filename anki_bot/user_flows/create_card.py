from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentTypes
from aiogram.types import Message

from anki_bot.models import BotAnkiCard
from anki_bot.states import CreateCardState
from anki_bot.user_flows.list_decks import process_list_decks_command
from anki_bot.user_flows.main_menu import process_return_to_main_menu
from anki_bot.user_interface import MainMenu
from anki_logic import AnkiApp


class CreateCardFlow:

    anki: AnkiApp

    def __init__(self, dp: Dispatcher, anki: AnkiApp):
        CreateCardFlow.anki = anki
        dp.register_message_handler(
            process_add_card_command,
            text=MainMenu.BTN_CREATE,
        )
        dp.register_message_handler(
            process_side_1,
            state=CreateCardState.wait_side_1,
            content_types=ContentTypes.TEXT | ContentTypes.PHOTO,
        )
        dp.register_message_handler(
            process_side_2,
            state=CreateCardState.wait_side_2,
            content_types=ContentTypes.TEXT | ContentTypes.PHOTO,
        )
        dp.register_message_handler(
            process_deck_selection,
            state=CreateCardState.wait_deck_selection,
        )

        # Add handlers for other content types HERE

        dp.register_message_handler(  # Strongly last, all other content types handler
            process_wrong_content_type,
            content_types=ContentTypes.ANY,
            state=CreateCardState.wait_side_1,
        )
        dp.register_message_handler(
            process_wrong_content_type,
            content_types=ContentTypes.ANY,
            state=CreateCardState.wait_side_2,
        )


async def process_add_card_command(message: Message, state: FSMContext):
    if await CreateCardFlow.anki.list_decks_names():
        await CreateCardState.wait_side_1.set()
        await message.answer("Введите первую сторону карточки")
    else:
        await message.answer("У вас нет колод")
        await process_return_to_main_menu(message, state)


async def process_side_1(message: Message, state: FSMContext):
    async with state.proxy() as data:
        card = BotAnkiCard(
            side_1_txt=message.text,
            side_1_img=message.photo.pop().file_id if message.photo else None,
        )
        data["created_card"] = card
        await CreateCardState.wait_side_2.set()
        await message.answer("Введите вторую сторону карточки")


async def process_side_2(message: Message, state: FSMContext):
    async with state.proxy() as data:
        card: BotAnkiCard = data["created_card"]
        card.side_2_txt = message.text
        card.side_2_img = message.photo.pop().file_id if message.photo else None
    await process_list_decks_command(message, state)
    await CreateCardState.wait_deck_selection.set()
    async with state.proxy() as data:
        data["created_card"] = card


async def process_deck_selection(message: Message, state: FSMContext):
    async with state.proxy() as data:
        card: BotAnkiCard = data["created_card"]
        if deck_id := await CreateCardFlow.anki.get_deck_id_by_name(message.text):
            card.deck_id = deck_id
            await CreateCardFlow.anki.create_card(**card.dict())
            await message.answer(f"Карточка создана")
            await process_return_to_main_menu(message, state)
        else:
            await message.answer("Такой колоды нет")
            return


async def process_wrong_content_type(message: Message, state: FSMContext):
    await message.answer("Неверный формат сообщения")
    await process_return_to_main_menu(message, state)
