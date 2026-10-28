from dataclasses import dataclass

@dataclass(frozen=True)
class WebGameField:
    cells: tuple[tuple[int, ...], ...]
