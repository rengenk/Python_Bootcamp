from dataclasses import dataclass

@dataclass(frozen=True)
class DataGameField:
    cells: tuple[tuple[int, ...], ...]
