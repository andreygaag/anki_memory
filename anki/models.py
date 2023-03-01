from typing import Optional

from pydantic import BaseModel
from pydantic import Field


class AnkiCard(BaseModel):
    side_1: int
    side_2: int
    yes: int = 0
    no: int = 0
    show_time: Optional[int] = None
    create_time: int
