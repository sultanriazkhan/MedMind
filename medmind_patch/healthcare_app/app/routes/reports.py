from flask import Blueprint, render_template, request, jsonify
import requests

reports_bp = Blueprint("reports", __name__, url_prefix="/reports")

FASTAPI_PROCESS_URL = "http://127.0.0.1:8000/process"


@reports_bp.route("/upload", methods=["GET"])
def upload_report():
    return render_template("reports/upload_report.html")


@reports_bp.route("/analyze", methods=["POST"])
def analyze_report():
    try:
        text_input = request.form.get("text_input")
        uploaded_file = request.files.get("file")

        if uploaded_file and uploaded_file.filename:
            response = requests.post(
                FASTAPI_PROCESS_URL,
                files={
                    "file": (
                        uploaded_file.filename,
                        uploaded_file.stream,
                        uploaded_file.content_type,
                    )
                },
                timeout=120,
            )

        elif text_input and text_input.strip():
            response = requests.post(
                FASTAPI_PROCESS_URL,
                data={"text_input": text_input},
                timeout=120,
            )

        else:
            return jsonify({
                "success": False,
                "error": "Please upload a report file or enter report text."
            }), 400

        try:
            return jsonify(response.json()), response.status_code
        except Exception:
            return jsonify({
                "success": False,
                "error": "FastAPI returned an invalid response.",
                "raw_response": response.text,
            }), 500

    except requests.exceptions.ConnectionError:
        return jsonify({
            "success": False,
            "error": "FastAPI backend is not running. Start it using: python run.py"
        }), 503

    except requests.exceptions.Timeout:
        return jsonify({
            "success": False,
            "error": "Processing timed out. Try a smaller file or text input."
        }), 504

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@reports_bp.route("/processing")
def processing():
    return render_template("reports/processing.html")


@reports_bp.route("/analysis-overview")
def analysis_overview():
    return render_template("reports/analysis_overview.html")


@reports_bp.route("/history")
def report_history():
    return render_template("reports/report_history.html")


@reports_bp.route("/test-explanation")
def test_explanation():
    return render_template("reports/test_explanation.html")