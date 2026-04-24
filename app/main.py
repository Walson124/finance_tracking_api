import os

from flask import Flask
from flask_cors import CORS
from app.routes.routes import main_bp
from app.connections.psql_connector import psql_connector  # Assuming you're using Blueprints

app = Flask(__name__)

# Enable CORS for specific origins
CORS(app, resources={r"/*": {"origins": ["http://localhost:3001", "http://frontend:3001"]}})

app.config['CACHE_TYPE'] = 'SimpleCache'

# Register your blueprint, if you have one
app.register_blueprint(main_bp)

app.config['connector'] = psql_connector()

@app.route('/test', methods=['POST'])
def test():
    print(os.getenv('DB_NAME'))
    return 'test'

# Make sure to NOT use app.run() in production mode
if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=5001)  # This is only for local development, NOT for production
