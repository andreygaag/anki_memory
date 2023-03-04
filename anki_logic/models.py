import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import Field
from pydantic import root_validator
from pydantic import validator


class AnkiDeck(BaseModel):
    deck_id: Optional[int]
    name: str
    show_time: Optional[datetime.datetime]
    create_time: Optional[datetime.datetime]


class AnkiCard(BaseModel):
    card_id: Optional[int]
    side_1_img: Optional[str]
    side_1_txt: Optional[str]
    side_2_img: Optional[str]
    side_2_txt: Optional[str]
    yes: Optional[int] = 0
    no: Optional[int] = 0
    show_time: Optional[datetime.datetime]
    create_time: Optional[datetime.datetime]
    deck_id: int

    @validator("side_1_txt", always=True)
    def side_1_image_or_text_required(cls, v, values):
        if not v and not values.get("side_1_img"):
            raise ValueError("side_1_img or side_1_txt is required")
        return v

    @validator("side_2_txt", always=True)
    def side_2_image_or_text_required(cls, v, values):
        if not v and not values.get("side_2_img"):
            raise ValueError("side_2_img or side_2_txt is required")
        return v
