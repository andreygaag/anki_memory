import logging
import os
from typing import Any

from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from aiogram.types import Message
from aiogram.types import Update


class StateLoggingMiddleware(LifetimeControllerMiddleware):
    async def pre_process(self, message: Message, data, *args):
        pass

    async def post_process(self, message: Message, data, *args):
        if state := data.get("state"):
            current_state = await state.get_state()
            logging.info(f"Post state: {current_state}")

    async def on_process_message(self, message: Message, data: dict[str, Any]):
        state = await data["state"].get_state()
        logging.info(f"Pre state: {state}")
        logging.info(f"Message: {message.text}")


class OnlyCreatorCanLaunchMiddleware(LifetimeControllerMiddleware):
    async def pre_process(self, update: Update | Message, data, *args):
        if isinstance(update, Update):
            message = update.message
        else:
            message = update
        if message.from_user.id != int(os.getenv("TELEGRAM_ADMIN_ID", 0)):
            await message.answer(
                f"Ваш telegram id: {message.from_user.id}. Это пока не общественный бот, только создатель может запускать. Скоро будет публичный.",
            )
            raise CancelHandler()
