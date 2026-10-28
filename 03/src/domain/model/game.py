from dataclasses import dataclass
from uuid import UUID
from .game_field import GameField

@dataclass(frozen=True)
class Game:
    game_id: UUID
    field: GameField
