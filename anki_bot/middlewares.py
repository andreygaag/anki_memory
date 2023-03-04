import logging
from typing import Any

from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from aiogram.types import Message


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
