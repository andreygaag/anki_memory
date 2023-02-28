from typing import Optional

from sqlalchemy.orm import DeclarativeBase, MappedColumn
from sqlalchemy.orm import Mapped


class Base(DeclarativeBase):
    pass

class AnkiCardsTable(Base):
    __tablename__ = 'anki_cards'
    id: Mapped[int] = MappedColumn(primary_key=True)
    side_1_msg: Mapped[int]
    side_2_msg: Mapped[int]
    yes: Mapped[int]
    no: Mapped[int]
    show_time: Mapped[Optional[int]]
    create_time: Mapped[int]