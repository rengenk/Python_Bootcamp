from domain.model.game import Game
from domain.model.game_field import GameField
from domain.service.game_service import GameService

class MinimaxGameService(GameService):
    USER = 1
    COMPUTER = 2

    def next_move(self, field: GameField) -> GameField:
        if self.is_finished(field):
            return field
        board = [list(row) for row in field.cells]
        best_score = float("-inf")
        best_move = None
        for r in range(3):
            for c in range(3):
                if board[r][c] == 0:
                    board[r][c] = self.COMPUTER
                    score = self._minimax(board, False)
                    board[r][c] = 0
                    if score > best_score:
                        best_score, best_move = score, (r, c)
        if best_move is not None:
            board[best_move[0]][best_move[1]] = self.COMPUTER
        return GameField(tuple(tuple(row) for row in board))

    def _minimax(self, board, maximizing):
        winner = self._winner(board)
        if winner == self.COMPUTER:
            return 1
        if winner == self.USER:
            return -1
        if all(cell != 0 for row in board for cell in row):
            return 0
        if maximizing:
            best = float("-inf")
            for r in range(3):
                for c in range(3):
                    if board[r][c] == 0:
                        board[r][c] = self.COMPUTER
                        best = max(best, self._minimax(board, False))
                        board[r][c] = 0
            return best
        best = float("inf")
        for r in range(3):
            for c in range(3):
                if board[r][c] == 0:
                    board[r][c] = self.USER
                    best = min(best, self._minimax(board, True))
                    board[r][c] = 0
        return best

    def validate_field(self, previous: Game, submitted: GameField) -> None:
        old = previous.field.cells
        new = submitted.cells
        if self.is_finished(previous.field):
            raise ValueError("The game has already ended")
        changed = [(r, c) for r in range(3) for c in range(3) if old[r][c] != new[r][c]]
        if len(changed) != 1:
            raise ValueError("Allow exactly one new user move")
        r, c = changed[0]
        if old[r][c] != 0 or new[r][c] != self.USER:
            raise ValueError("You can only change an empty cell by putting 1")
        if any(old[i][j] != new[i][j] for i in range(3) for j in range(3) if (i, j) != (r, c)):
            raise ValueError("Previous moves cannot be changed")
        if self._winner([list(row) for row in new]) != 0 and not self.is_finished(submitted):
            raise ValueError("Invalid game state")

    def is_finished(self, field: GameField) -> bool:
        return field.winner() != 0 or field.is_full()

    @staticmethod
    def _winner(board):
        lines = list(board)
        lines += [[board[r][c] for r in range(3)] for c in range(3)]
        lines += [[board[i][i] for i in range(3)], [board[i][2-i] for i in range(3)]]
        for line in lines:
            if line[0] != 0 and line.count(line[0]) == 3:
                return line[0]
        return 0
