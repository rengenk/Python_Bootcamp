from dataclasses import dataclass

@dataclass(frozen=True)
class GameField:
    cells: tuple[tuple[int, ...], ...]

    def __post_init__(self):
        if len(self.cells) != 3 or any(len(row) != 3 for row in self.cells):
            raise ValueError("The game field must be of a size 3x3")
        if any(cell not in (0, 1, 2) for row in self.cells for cell in row):
            raise ValueError("Field cells can only contain 0, 1 or 2")

    @classmethod
    def empty(cls):
        return cls(((0, 0, 0), (0, 0, 0), (0, 0, 0)))

    def to_list(self):
        return [list(row) for row in self.cells]

    def winner(self):
        lines = list(self.cells)
        lines += [[self.cells[r][c] for r in range(3)] for c in range(3)]
        lines += [[self.cells[i][i] for i in range(3)],
                  [self.cells[i][2 - i] for i in range(3)]]
        for line in lines:
            if line[0] != 0 and line.count(line[0]) == 3:
                return line[0]
        return 0

    def is_full(self):
        return all(cell != 0 for row in self.cells for cell in row)
