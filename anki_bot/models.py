from typing import Optional

from pydantic import BaseModel


class BotAnkiCard(BaseModel):
    side_1_txt: Optional[str]
    side_1_img: Optional[str]
    side_2_txt: Optional[str]
    side_2_img: Optional[str]
    deck_id: Optional[int]


# TODO: Use
class BotAnkiDeck(BaseModel):
    name: Optional[str]
