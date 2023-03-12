import random
from typing import Optional

from anki_logic.models import AnkiCard
from anki_logic.models import AnkiDeck
from database import PgDatabase


class AnkiApp:
    db: PgDatabase
    __slots__ = ("cards", "decks", "decks_by_name")

    @classmethod
    async def create(cls, db):
        self = cls()
        AnkiApp.db = db
        await self._refresh_cards()
        await self._refresh_decks()
        return self

    async def next_card(self):
        return await self.random_card()

    async def get_random_card_from_deck(self, deck_id: int) -> Optional[AnkiCard]:
        # TODO: Optimisation, update show counter and last show time
        cards = [card for card in self.cards.values() if card.deck_id == deck_id]
        return random.choice(cards) if cards else None

    async def get_random_card(self) -> AnkiCard:
        all_cards = self.cards.values()
        return random.choice(list(all_cards)) if all_cards else None

    async def get_deck_by_name(self, name: str) -> Optional[AnkiDeck]:
        return self.decks_by_name.get(name)

    async def get_deck_id_by_name(self, name: str) -> Optional[int]:
        deck = await self.get_deck_by_name(name)
        return deck.deck_id if deck else None

    async def list_decks(self) -> dict[int, AnkiDeck]:
        return self.decks

    async def list_decks_names(self) -> list[str]:
        return self.decks_by_name.keys()

    async def create_card(self, **kwargs):
        card = AnkiCard(**kwargs)
        await self.db.create_card(**card.dict())
        await self._refresh_cards()

    async def create_deck(self, name: str):
        await AnkiApp.db.create_deck(name)
        await self._refresh_decks()

    async def delete_card(self, card_id: int):
        await AnkiApp.db.delete_card(card_id)
        await self._refresh_cards()

    async def delete_deck(self, deck_id: int):
        await AnkiApp.db.delete_deck(deck_id)
        await self._refresh_decks()

    async def update_card(self, card: AnkiCard):
        await AnkiApp.db.update_card(card)

    async def update_deck(self, deck: AnkiDeck):
        raise NotImplemented

    async def _refresh_cards(self):
        self.cards = {card.card_id: card for card in await self.db.list_cards()}

    async def _refresh_decks(self):
        self.decks = {deck.deck_id: deck for deck in await self.db.list_decks()}
        self.decks_by_name = {deck.name: deck for deck in self.decks.values()}
