import asyncio
import logging
import os
import sys
from asyncio import Future

import uvloop

from anki import Anki
from database import Database
from tg_bot import Bot


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
        self.bot = await Bot.create(self.anki)
        self.logger.info("AnkiMemory telegram app")
        return self


async def main():
    anki_memory_app = await AnkiMemoryApp.create()

if __name__ == "__main__":
    if sys.version_info >= (3, 11):
        with asyncio.Runner(loop_factory=uvloop.new_event_loop) as runner:
            runner.run(main())
    else:
        uvloop.install()
        asyncio.run(main())
