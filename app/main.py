from flask import Flask
from flask_cors import CORS
from app.routes.routes import main_bp
from app.connections.psql_connector import psql_connector

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": ["http://localhost:3001", "http://frontend:3001"]}})

app.register_blueprint(main_bp)

app.config['connector'] = psql_connector()

if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=5001)
