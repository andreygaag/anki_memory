""" Database layer """
import logging
import time

from sqlalchemy import (
    MetaData,
    select,
    insert,
    update,
)
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from database.tables import Base, AnkiCardsTable


class Database:
    @classmethod
    async def create(cls, host: str, user: str, password: str, db_name: str):
        self = Database()
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

    async def get_cards(self):
        async with self.session() as session:
            async with session.begin():
                result = await session.execute(
                    select(AnkiCardsTable).order_by(AnkiCardsTable.create_time)
                )
                return result.scalars().all()

    async def get_card(self, card_id: int = None):
        async with self.session() as session:
            async with session.begin():
                result = await session.execute(
                    select(AnkiCardsTable).where(AnkiCardsTable.id == card_id)
                )
                return result.scalars().first()

    async def create_card(self, card) -> None:
        self.logger.info("Create new card in database")
        async with self.session() as session:
            async with session.begin():
                await session.execute(
                    insert(AnkiCardsTable).values(
                        side_1_msg=card.side_1,
                        side_2_msg=card.side_2,
                        yes=card.yes,
                        no=card.no,
                        show_time=card.show_time,
                        create_time=card.create_time,
                    )
                )

    async def update_card(self, card):
        async with self.session() as session:
            async with session.begin():
                update(AnkiCardsTable).where(AnkiCardsTable.id == card.id).values(
                    side_1=card.side_1,
                    side_2=card.side_2,
                    yes=card.yes,
                    no=card.no,
                    show_time=None,
                    create_time=int(time.time()),
                )
