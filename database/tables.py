import datetime
from typing import Optional

from sqlalchemy import CheckConstraint
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import func
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import MappedColumn


class Base(DeclarativeBase):
    pass


class AnkiDecksTable(Base):
    __tablename__ = "decks"
    deck_id: Mapped[int] = MappedColumn(primary_key=True)
    name: Mapped[str]
    show_time: Mapped[Optional[datetime.datetime]] = MappedColumn(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    created_time: Mapped[datetime.datetime] = MappedColumn(
        DateTime(timezone=True),
        server_default=func.now(),
    )


class AnkiCardsTable(Base):
    __tablename__ = "cards"
    card_id: Mapped[int] = MappedColumn(primary_key=True)
    side_1_txt: Mapped[Optional[str]] = MappedColumn(String(4096))
    side_1_img: Mapped[Optional[str]] = MappedColumn(String(256))
    side_2_txt: Mapped[Optional[str]] = MappedColumn(String(4096))
    side_2_img: Mapped[Optional[str]] = MappedColumn(String(256))
    yes: Mapped[int] = MappedColumn(default=0)
    no: Mapped[int] = MappedColumn(default=0)
    show_time: Mapped[Optional[datetime.datetime]] = MappedColumn(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    created_time: Mapped[datetime.datetime] = MappedColumn(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    deck_id: Mapped[int] = MappedColumn(ForeignKey("decks.deck_id"))

    __table_args__ = (
        CheckConstraint("NOT (side_1_txt IS NULL AND side_1_img IS NULL)"),
        CheckConstraint("NOT (side_2_txt IS NULL AND side_2_img IS NULL)"),
    )
