from dataclasses import dataclass
from uuid import UUID
from datasource.model.game_field import DataGameField

@dataclass(frozen=True)
class DataGame:
    game_id: UUID
    field: DataGameField
