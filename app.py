from flask import Flask, request, jsonify, Response
import os
import json
from utils.runner_parser import get_runner_result
from datetime import datetime
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

# 기존 /result는 유지
@app.route("/result", methods=["GET"])
def get_result():
    usedata = request.args.get("usedata")
    bib = request.args.get("bib")
    if not usedata or not bib:
        return jsonify({"error": "usedata와 bib 쿼리 파라미터가 필요합니다."}), 400
    result = get_runner_result(usedata, bib)
    return jsonify(result)

# ✅ 새로 추가: SmartChip 대회 리스트 제공
@app.route("/races", methods=["GET"])
def get_smartchip_races():
    today = datetime.today().strftime("%Y-%m-%d")
    filepath = f"output/events_{today}.json"
    if not os.path.exists(filepath):
        return jsonify({"error": f"No race list found for {today}"}), 404

    with open(filepath, "r", encoding="utf-8") as f:
        races = json.load(f)

    return jsonify(races)

@app.route("/")
def index():
    return {
        "message": "K-TRACKER SmartChip API is running.",
        "endpoints": ["/result?usedata=...&bib=...", "/races"]
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
