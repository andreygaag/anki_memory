import logging
import time
import random

from anki.models import AnkiCard


class Anki:
    def __init__(self, db):
        self.logger = logging.getLogger(__name__)
        self.db = db
        self.logger.info("Initializing Anki")

    async def next_card(self):
        self.logger.info("Getting next card")
        return await self.get_card(1)

    async def random_card(self) -> tuple[int, int]:
        self.logger.info("Getting random card")
        # TODO: optimisation
        all_cards = await self.db.get_cards()
        random_card = all_cards[random.randint(0, len(all_cards) - 1)]
        return random_card.side_2_msg, random_card.side_1_msg

    async def get_card(self, card_id: int = None) -> tuple[int, int]:
        self.logger.info("Getting cards")
        return await self.db.get_cards()

    async def create_card(self, side_1: int, side_2: int):
        self.logger.info("Adding card")
        data = {
            "side_1": side_1,
            "side_2": side_2,
            "yes": 0,
            "no": 0,
            "show_time": None,
            "create_time": int(time.time()),
        }
        card = AnkiCard(**data)
        return await self.db.create_card(card)

    async def update_card(self, card: AnkiCard):
        self.logger.info("Updating card")
        return await self.db.update_card(card)

