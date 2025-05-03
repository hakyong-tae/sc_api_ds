from flask import Flask, jsonify, request
from flask_cors import CORS
from utils.runner_parser import get_runner_result
import os
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return jsonify({
        "status": "K-TRACKER SmartChip API is running.",
        "available_endpoints": ["/races", "/result"]
    })

@app.route("/result")
def result():
    usedata = request.args.get("usedata")
    bib = request.args.get("bib")
    
    if not usedata or not bib:
        return jsonify({"error": "Missing usedata or bib parameter"}), 400

    result = get_runner_result(usedata, bib)
    return jsonify(result)

@app.route("/races")
def races():
    today = datetime.now().strftime("%Y-%m-%d")
    filepath = f"output/events_{today}.json"
    
    if not os.path.exists(filepath):
        return jsonify({"error": "No race file for today."}), 404

    with open(filepath, "r", encoding="utf-8") as f:
        races = json.load(f)
    
    return jsonify(races)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
