
def parse_response(ai_text):

    meaning = ""
    causes = ""
    effects = ""
    solution = ""

    lines = ai_text.split("\n")

    for line in lines:

        clean_line = line.strip()

        if clean_line.lower().startswith("meaning:"):
            meaning = clean_line.replace("Meaning:", "").strip()

        elif clean_line.lower().startswith("causes:"):
            causes = clean_line.replace("Causes:", "").strip()

        elif clean_line.lower().startswith("effects:"):
            effects = clean_line.replace("Effects:", "").strip()

        elif clean_line.lower().startswith("solution:"):
            solution = clean_line.replace("Solution:", "").strip()

    if not meaning:
        meaning = "Could not parse meaning"

    if not causes:
        causes = "Could not parse causes"

    if not effects:
        effects = "Could not parse effects"

    if not solution:
        solution = "Consult healthcare professional"

    return {
        "meaning": meaning,
        "causes": causes,
        "effects": effects,
        "solution": solution
    }