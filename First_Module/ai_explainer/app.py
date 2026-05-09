from flask import Flask, request, jsonify
from ai_explainer_restricted import explain_full_report

app = Flask(__name__)


@app.route('/')
def home():
    return "AI Explanation Module Running Successfully"


@app.route('/generate-explanations', methods=['POST'])
def generate_explanations():

    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "error": "No JSON payload provided"
            }), 400

        results = explain_full_report(data)

        return jsonify(results)

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)