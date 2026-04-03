from flask import Flask, request, jsonify
import json
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home():
    with open("index.html", encoding="utf-8") as f:
        return f.read()


DATA_FILE = "data.json"

# создать файл если нет
def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


@app.route("/add", methods=["POST"])
def add_entry():
    data = load_data()

    activities = request.json.get("activities")

    score = len(activities)

    new_entry = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "mood": request.json.get("mood"),
        "activities": activities,
        "score": score
    }

    data.append(new_entry)
    save_data(data)

    return jsonify({"status": "saved"})


@app.route("/logs", methods=["GET"])
def get_logs():
    return jsonify(load_data())


@app.route("/stats")
def stats():
    data = load_data()

    total = len(data)
    good_days = sum(1 for d in data if d["mood"] == "good")

    return {
        "total_days": total,
        "good_days": good_days
    }


import os

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))