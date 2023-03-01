import asyncio
import logging
import os
import sys
from asyncio import Future

from anki import Anki
from database import Database
from tg_bot import TelegramBot


class AnkiMemoryApp:

    @classmethod
    async def create(cls):
        self = AnkiMemoryApp()
        self.logger = logging.getLogger(__name__)
        self.logger.info("Starting AnkiMemory app")
        self.database = await Database.create(
            host=os.getenv("POSTGRES_HOST"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            db_name=os.getenv("POSTGRES_DB"),
        )
        self.anki = Anki(self.database)
        self.bot = await TelegramBot.create(self.anki)
        self.logger.info("AnkiMemory telegram app")
        return self


async def main():
    anki_memory_app = await AnkiMemoryApp.create()

if __name__ == "__main__":
    asyncio.run(main())
