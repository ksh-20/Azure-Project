from flask import Flask, jsonify
from flask_cors import CORS

from backend.repository import fetch_repositories

app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route("/api/repos", methods=["GET"])
def get_repositories():
    result = fetch_repositories()
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)