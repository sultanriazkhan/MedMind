import requests
import time

from parser_utils import parse_response
from prompt_builder import build_prompt

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "mistral"
TIMEOUT = 120
MAX_RETRIES = 3



def call_ollama(prompt):

    for attempt in range(MAX_RETRIES):

        try:
            response = requests.post(
                OLLAMA_URL,
                json={
                    "model": MODEL_NAME,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.2,
                        "top_p": 0.9,
                        "num_predict": 150
                    }
                },
                timeout=TIMEOUT
            )

            data = response.json()

            if "response" not in data:
                continue

            return data["response"].strip()

        except Exception:
            time.sleep(2)

    return None



def get_ai_explanation(test_name=None, value=None, status=None):

    if not test_name:
        return {
            "error": "test_name is required"
        }

    prompt = build_prompt(test_name, value, status)

    raw_output = call_ollama(prompt)

    if not raw_output:
        return {
            "test_name": test_name,
            "value": value,
            "status": status,
            "meaning": "Not available",
            "causes": "Not available",
            "effects": "Not available",
            "solution": "Consult doctor"
        }

    parsed = parse_response(raw_output)

    return {
        "test_name": test_name,
        "value": value,
        "status": status,
        **parsed
    }



def explain_full_report(test_list):

    results = []

    BATCH_SIZE = 5

    for i in range(0, len(test_list), BATCH_SIZE):

        batch = test_list[i:i+BATCH_SIZE]

        for test in batch:

            result = get_ai_explanation(
                test.get("test_name"),
                test.get("value"),
                test.get("status")
            )

            results.append(result)

            time.sleep(1)

    return {
        "report": results,
        "total_tests": len(results),
        "generated_by": "AI Explanation Module"
    }
    