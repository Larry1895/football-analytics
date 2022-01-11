from flask import Blueprint
import json

from src.scrapper.repositories.position_repository import find_number_of_players_per_position

app_position_distribution = Blueprint('app_position_distribution', __name__)


@app_position_distribution.route("/positions/distribution")
def positions_distribution():
    data = find_number_of_players_per_position()

    return json.dumps([(dict(row)) for row in data])
