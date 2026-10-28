from uuid import UUID
from flask import Blueprint, jsonify, request
from domain.model.game_field import GameField
from web.mapper.game_mapper import WebGameMapper

def create_game_blueprint(game_module):
    blueprint = Blueprint("games", __name__)

    def serialize(game):
        web_game = WebGameMapper.to_web(game, game_module.is_finished(game))
        return {"uuid": str(web_game.game_id),
                "field": [list(row) for row in web_game.field.cells],
                "finished": web_game.finished}

    @blueprint.post("/game/<game_id>")
    def play(game_id):
        try:
            parsed_id = UUID(game_id)
            payload = request.get_json(silent=True)
            if not isinstance(payload, dict) or "field" not in payload:
                return jsonify({"error": "A JSON object with a 3x3 field is expected"}), 400
            raw_field = payload["field"]
            if not isinstance(raw_field, list) or len(raw_field) != 3 or any(
                not isinstance(row, list) or len(row) != 3 for row in raw_field
            ):
                return jsonify({"error": "The field must be of a size 3x3"}), 400
            if any(type(cell) is not int or cell not in (0, 1, 2)
                   for row in raw_field for cell in row):
                return jsonify({"error": "Cells can contain only integers 0, 1 or 2"}), 400
            field = GameField(tuple(tuple(row) for row in raw_field))
            game = game_module.play(parsed_id, field)
            return jsonify(serialize(game)), 200
        except ValueError as error:
            return jsonify({"error": str(error)}), 400
        except LookupError as error:
            return jsonify({"error": str(error)}), 404

    @blueprint.post("/game")
    def create():
        game = game_module.create_game()
        return jsonify(serialize(game)), 201

    return blueprint
