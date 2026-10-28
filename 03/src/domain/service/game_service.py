from abc import ABC, abstractmethod
from uuid import UUID
from domain.model.game import Game
from domain.model.game_field import GameField

class GameService(ABC):
    @abstractmethod
    def next_move(self, field: GameField) -> GameField:
        """Returned the field after the computers turn"""

    @abstractmethod
    def validate_field(self, previous: Game, submitted: GameField) -> None:
        """Verifies that the user has made exactly one valid move"""

    @abstractmethod
    def is_finished(self, field: GameField) -> bool:
        """Checks for the end of the game"""
