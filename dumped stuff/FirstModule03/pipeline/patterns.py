"""
pipeline/patterns.py

Reusable compiled regex patterns for pathology report extraction.

Handles: decimals, negative values, comparison operators, percentages,
scientific notation, OCR spacing issues, and common report row formats.
"""

import re

# ---------------------------------------------------------------------------
# Atomic Building Blocks
# ---------------------------------------------------------------------------

# Numeric value: supports negatives, decimals, scientific notation, e.g.
#   13.5   -0.5   1.2e3   1.2E-4   126
_NUM = r"-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?"

# Comparison operator prefix, e.g. ">", ">=", "<", "<=", "~", "≤", "≥"
_CMP = r"[<>]=?|[~≤≥]"

# ---------------------------------------------------------------------------
# Primary Patterns
# ---------------------------------------------------------------------------

VALUE_PATTERN = re.compile(
    r"""
    (?P<operator>[<>]=?|[~≤≥])?   # optional comparison operator
    \s*
    (?P<value>""" + _NUM + r""")   # numeric value (incl. negatives & sci notation)
    \s*
    (?P<percent>%)?                # optional trailing percent sign
    """,
    re.VERBOSE
)
"""
Matches a standalone numeric value with optional operator and percent.

Groups:
    operator  - comparison prefix (<, >, <=, >=, ~, ≤, ≥) or None
    value     - the numeric string
    percent   - '%' if present

Examples:
    "13.5"       -> value=13.5
    ">126"       -> operator='>', value=126
    "1.2e3"      -> value=1200.0
    "-0.5"       -> value=-0.5
    "95%"        -> value=95, percent='%'
"""


RANGE_PATTERN = re.compile(
    r"""
    (?P<low>""" + _NUM + r""")     # lower bound of range
    \s*
    (?:-|to|–|—)                   # separator: hyphen, 'to', en-dash, em-dash
    \s*
    (?P<high>""" + _NUM + r""")    # upper bound of range
    """,
    re.VERBOSE | re.IGNORECASE
)
"""
Matches a numeric reference range, e.g. "3.5 - 5.0", "70 to 110", "4.5–6.5".

Groups:
    low   - lower bound string
    high  - upper bound string

Examples:
    "3.5 - 5.0"    -> low='3.5', high='5.0'
    "70 to 110"    -> low='70', high='110'
    "4.5–6.5"      -> low='4.5', high='6.5'
"""


UNIT_PATTERN = re.compile(
    r"""
    \b
    (?P<unit>
        g/?dL |                    # g/dL, gm/dL, g/dl
        gm/?dL |
        mg/?dL |                   # mg/dL
        mg/? [Ll] |               # mg/L
        [uU][gG]/?dL |             # ug/dL, mcg/dL
        [nN][gG]/?[mM][lL] |       # ng/mL
        [pP][gG]/?[mM][lL] |       # pg/mL
        [mM][iI][uU]/?[mM][lL] |  # mIU/mL
        [uU][iI][uU]/?[mM][lL] |  # uIU/mL
        [iI][uU]/?[lL] |           # IU/L
        [uU]/?[lL] |               # U/L
        m[Ee][qQ]/?[lL] |          # mEq/L
        mmol/?[lL] |               # mmol/L
        [uU]mol/?[lL] |            # umol/L
        nmol/?[lL] |               # nmol/L
        pmol/?[lL] |               # pmol/L
        10\^[36]/?[uU][lL] |       # 10^3/uL, 10^6/uL
        [kK]/?[uU][lL] |           # k/uL
        /[uU][lL] |                # /uL
        /[cC][uU][mM][mM] |        # /cumm
        /[mM][mM]3 |               # /mm3
        /[hH][pP][fF] |            # /hpf
        [fF][lL] |                 # fL
        \bpg\b |                   # pg (picograms, standalone)
        mm/?hr |                   # mm/hr
        mm/?[hH] |                 # mm/h
        [sS]ec(?:onds?)? |         # sec, secs, seconds
        [nN][gG]/?[dD][lL] |       # ng/dL
        [uU][gG]/?[lL] |           # ug/L
        [gG]/?[lL] |               # g/L
        [mM][lL]/?min(?:/1\.73m2)? # mL/min or mL/min/1.73m2
    )
    \b
    """,
    re.VERBOSE
)
"""
Matches common pathology unit strings anywhere in text.

Group:
    unit  - the matched unit string

Examples:
    "g/dL"          -> unit='g/dL'
    "/cumm"         -> unit='/cumm'
    "mIU/mL"        -> unit='mIU/mL'
    "10^3/uL"       -> unit='10^3/uL'
    "mm/hr"         -> unit='mm/hr'
"""


FLAG_PATTERN = re.compile(
    r"""
    \b
    (?P<flag>
        H(?:igh)?  |               # H, High
        L(?:ow)?   |               # L, Low
        \*+        |               # * or ** or ***
        \bAbn(?:ormal)?\b |        # Abn, Abnormal
        \bCrit(?:ical)?\b |        # Crit, Critical
        \bPOSITIVE\b |             # POSITIVE
        \bNEGATIVE\b |             # NEGATIVE
        \bREACTIVE\b |             # REACTIVE
        \bNR\b                     # NR (not reactive)
    )
    \b
    """,
    re.VERBOSE | re.IGNORECASE
)
"""
Matches abnormality flags commonly found in pathology reports.

Group:
    flag  - the flag string (H, L, *, Abn, Critical, POSITIVE, NEGATIVE, etc.)

Examples:
    "13.5 H"     -> flag='H'
    "0.02 *"     -> flag='*'
    "POSITIVE"   -> flag='POSITIVE'
"""


TEST_VALUE_PATTERN = re.compile(
    r"""
    (?P<test_name>[A-Za-z][A-Za-z0-9\s\-/\.()]+?)  # test name (greedy but bounded)
    \s*
    [:=]\s*                                          # separator: colon or equals
    (?P<operator>[<>]=?|[~≤≥])?                     # optional operator
    \s*
    (?P<value>""" + _NUM + r""")                    # numeric value
    \s*
    (?P<unit>                                        # optional unit
        [A-Za-z/%^*][A-Za-z0-9/%^.*\-]*
    )?
    """,
    re.VERBOSE
)
"""
Matches a test name followed by a colon/equals separator and a numeric value.

Groups:
    test_name  - raw test name text
    operator   - optional comparison operator
    value      - numeric value string
    unit       - optional unit string

Examples:
    "WBC : 12000 /uL"           -> test_name='WBC', value='12000', unit='/uL'
    "Glucose = >126 mg/dL"      -> test_name='Glucose', operator='>', value='126', unit='mg/dL'
    "Hb: 13.5 g/dL"             -> test_name='Hb', value='13.5', unit='g/dL'
"""


PATHOLOGY_ROW_PATTERN = re.compile(
    r"""
    ^
    (?P<test_name>[A-Za-z][A-Za-z0-9\s\-/()+%.]*?)  # test name at start of line
    \s*
    [:\-=|]?                                          # optional separator (colon, dash, pipe, equals)
    \s*
    (?P<operator>[<>]=?|[~≤≥])?                      # optional comparison operator
    \s*
    (?P<value>""" + _NUM + r""")                     # numeric value (required)
    \s*
    (?P<unit>[A-Za-z/%^*][A-Za-z0-9/%^.*\-]*)?      # optional unit
    \s*
    (?P<flag>[HLhl*]+|\bAbn\b|\bCrit\b)?             # optional flag
    \s*
    (?:                                               # optional reference range block
        (?:Ref(?:erence)?\.?\s*Range|RR|Ref|Normal)
        \s*[:\-]?\s*
        (?P<ref_low>""" + _NUM + r""")
        \s*(?:-|to|–)\s*
        (?P<ref_high>""" + _NUM + r""")
    )?
    \s*$
    """,
    re.VERBOSE | re.IGNORECASE
)
"""
Matches a complete pathology report row from start to end of line.

Groups:
    test_name   - test identifier at line start
    operator    - optional comparison operator
    value       - numeric result value (required)
    unit        - optional unit
    flag        - optional H/L/Abn/Crit flag
    ref_low     - lower reference range bound (optional)
    ref_high    - upper reference range bound (optional)

Examples:
    "Hb 13.5 g/dL H"
    "WBC : 12000 /uL"
    "Glucose >126 mg/dL Ref Range 70-110"
    "Platelets 450 10^3/uL Ref: 150-400"
"""
