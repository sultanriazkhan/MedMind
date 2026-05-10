from flask import Flask, request, jsonify
from explanation_engine import explain_full_report

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({
        "status": "success",
        "message": "Medical Explanation Engine Running"
    })


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "healthy"
    })


@app.route("/generate-explanations", methods=["POST"])
def generate_explanations():

    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "status": "error",
                "message": "No JSON payload provided"
            }), 400

        # Generate explanations from local knowledge base
        results = explain_full_report(data)

        return jsonify({
            "status": "success",
            "data": results
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5001,
        debug=True
    )