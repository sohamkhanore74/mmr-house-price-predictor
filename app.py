"""
MMR House Price Predictor - local web app.

Run:
    python app.py

Then open the link it prints (usually http://127.0.0.1:5000) in your browser.
"""
import numpy as np
import pandas as pd
import joblib
from flask import Flask, render_template, request, jsonify

bundle = joblib.load("model.joblib")
model = bundle["model"]
FEATURES = bundle["features"]
OPTIONS = bundle["options"]

app = Flask(__name__)


def format_inr(value):
    if value >= 1e7:
        return f"Rs {value / 1e7:.2f} Cr"
    return f"Rs {value / 1e5:.1f} Lakh"


@app.route("/")
def home():
    return render_template(
        "index.html",
        locations=[c.title() for c in OPTIONS["location"]],
        furnishings=OPTIONS["Furnishing"],
        transactions=OPTIONS["Transaction"],
        facings=OPTIONS["facing"],
        ownerships=OPTIONS["Ownership"],
    )


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    try:
        row = {
            "location": str(data["location"]).lower(),
            "area_sqft": float(data["area_sqft"]),
            "bhk": float(data["bhk"]),
            "Bathroom": float(data["bathroom"]),
            "Balcony": float(data["balcony"]),
            "floor_no": float(data["floor_no"]),
            "total_floors": float(data["total_floors"]),
            "parking": float(data["parking"]),
            "Furnishing": data["furnishing"],
            "Transaction": data["transaction"],
            "facing": data["facing"],
            "Ownership": data["ownership"],
        }
    except (KeyError, ValueError):
        return jsonify({"error": "Please fill in every field with a valid value."}), 400

    X = pd.DataFrame([row])[FEATURES]
    price = float(np.expm1(model.predict(X)[0]))

    return jsonify(
        {
            "price": format_inr(price),
            "low": format_inr(price * 0.85),
            "high": format_inr(price * 1.15),
        }
    )


if __name__ == "__main__":
    print("\nOpen this link in your browser:  http://127.0.0.1:5000\n")
    app.run(debug=False, port=5000)
