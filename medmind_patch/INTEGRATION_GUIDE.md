# MedMind Patient-Centered Explanation Integration

## 1. Add new files
Copy these files into your project:

```text
pipeline/interpreter.py
pipeline/report_summary.py
```

## 2. Replace/patch these existing files
Use the included versions or manually apply the changes:

```text
pipeline/extract.py
pipeline/validators.py
pipeline/confidence.py
main.py
data/units.json
```

## 3. Expected API result
After integration, every test will include:

```json
"patient_explanation": {
  "display_name": "White Blood Cell Count",
  "value_text": "7.4 10^3/uL",
  "status": "Normal",
  "severity": "none",
  "reference_range": "4.0 - 11.0 10^3/uL",
  "what_it_is": "White blood cells are part of your immune system and help fight infection.",
  "why_it_matters": "This value can rise with infection/inflammation...",
  "what_your_result_means": "Your white blood cell count is within the provided reference range...",
  "recommendation": "No immediate concern from this value alone."
}
```

## 4. Run

```bash
uvicorn main:app --reload
```

Then submit your sample CBC table.
