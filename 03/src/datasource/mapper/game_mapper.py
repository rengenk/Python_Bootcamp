from domain.model.game import Game
from domain.model.game_field import GameField
from datasource.model.game import DataGame
from datasource.model.game_field import DataGameField

class DataGameMapper:
    @staticmethod
    def to_data(game: Game) -> DataGame:
        return DataGame(game.game_id, DataGameField(game.field.cells))

    @staticmethod
    def to_domain(game: DataGame) -> Game:
        return Game(game.game_id, GameField(game.field.cells))
