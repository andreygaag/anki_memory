""" Database layer """
import logging
import time

from sqlalchemy import delete
from sqlalchemy import insert
from sqlalchemy import MetaData
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

from database.tables import AnkiCardsTable
from database.tables import AnkiDecksTable
from database.tables import Base


class PgDatabase:
    def __init__(self):
        self.engine = None
        self.session = None
        self.logger = None

    @classmethod
    async def create(cls, host: str, user: str, password: str, db_name: str):
        self = PgDatabase()
        self.logger = logging.getLogger(__name__)

        self.engine = create_async_engine(
            f"postgresql+asyncpg://{user}:{password}@{host}/{db_name}",
            echo=True,
        )

        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        self.session = async_sessionmaker(self.engine, expire_on_commit=False)

        self.logger.info("Initializing Database")
        return self

    async def list_cards(self):
        async with self.session() as session:
            async with session.begin():
                result = await session.execute(
                    select(AnkiCardsTable).order_by(
                        AnkiCardsTable.created_time,
                    ),
                )
                return result.scalars().all()

    async def list_decks(self):
        async with self.session() as session:
            async with session.begin():
                result = await session.execute(
                    select(AnkiDecksTable).order_by(
                        AnkiDecksTable.created_time,
                    ),
                )
                return result.scalars().all()

    async def get_card(self, card_id: int):
        async with self.session() as session:
            async with session.begin():
                result = await session.execute(
                    select(AnkiCardsTable).where(AnkiCardsTable.id == card_id),
                )
                return result.scalars().first()

    async def create_card(self, **card) -> None:
        self.logger.info("Create new card in database")
        async with self.session() as session:
            async with session.begin():
                await session.execute(
                    insert(AnkiCardsTable).values(
                        side_1_txt=card["side_1_txt"],
                        side_1_img=card["side_1_img"],
                        side_2_txt=card["side_2_txt"],
                        side_2_img=card["side_2_img"],
                        yes=card["yes"],
                        no=card["no"],
                        deck_id=card["deck_id"],
                    ),
                )

    async def create_deck(self, name) -> None:
        self.logger.info("Create new deck in database")
        async with self.session() as session:
            async with session.begin():
                await session.execute(
                    insert(AnkiDecksTable).values(
                        name=name,
                    ),
                )

    async def update_card_show_time(self, card):
        async with self.session() as session:
            async with session.begin():
                await session.execute(
                    update(AnkiCardsTable)
                    .where(AnkiCardsTable.card_id == card.card_id)
                    .values(
                        show_time=card.show_time,
                    ),
                )

    async def delete_card(self, card_id: int):
        async with self.session() as session:
            async with session.begin():
                await session.execute(
                    delete(AnkiCardsTable).where(
                        AnkiCardsTable.card_id == card_id,
                    ),
                )

    async def delete_deck(self, deck_id: int):
        async with self.session() as session:
            async with session.begin():
                await session.execute(
                    delete(AnkiDecksTable).where(
                        AnkiDecksTable.deck_id == deck_id,
                    ),
                )
