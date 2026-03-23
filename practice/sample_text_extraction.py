import fitz
import unicodedata
doc = fitz.open("test_pdf.pdf")
for page in doc:
    text=page.get_text()
    actual_text=unicodedata.normalize("NFKC", text)
    print(actual_text)