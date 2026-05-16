
def build_prompt(test_name=None, value=None, status=None):

    return f"""
Test: {test_name}
Value: {value}
Status: {status}

Explain in simple English in EXACT format:

Meaning: ...
Causes: ...
Effects: ...
Solution: ...

Rules:
- Keep short
- Keep medical language simple
- Focus only on provided test
- Avoid extra explanation
"""