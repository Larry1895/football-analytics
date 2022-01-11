from flask import Flask
from flask_cors import CORS

from position_distribution_chart_resource import app_position_distribution

main_app = Flask(__name__)
main_app.register_blueprint(app_position_distribution)
CORS(main_app)
