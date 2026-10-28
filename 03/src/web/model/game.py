from dataclasses import dataclass
from uuid import UUID
from web.model.game_field import WebGameField

@dataclass(frozen=True)
class WebGame:
    game_id: UUID
    field: WebGameField
    finished: bool = False
