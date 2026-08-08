from flask import Flask, jsonify, request

from recommendation_engine import rank_items
from validation import validate_recommendation_request

app = Flask(__name__)


@app.get("/health")
def health():
    return jsonify({"status": "ok"}), 200


@app.post("/recommendations")
def get_recommendations():
    payload = request.get_json(silent=True)

    errors = validate_recommendation_request(payload)

    if errors:
        first = errors[0]
        return jsonify({
            "error": "validation_error",
            "message": first["message"],
            "field": first["field"],
            "details": errors,
        }), 400

    recommendations = rank_items(
        payload["items"],
        payload["preferences"],
    )

    return jsonify({
        "recommendations": recommendations,
        "count": len(recommendations),
    }), 200


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8005, debug=True)
