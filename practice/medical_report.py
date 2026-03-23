import fitz
import unicodedata
doc= fitz.open("test_report.pdf")
for page in doc:
    tabs= page.find_tables()
    if tabs:
        for tab in tabs:
            table_data=tab.extract()
            for row in table_data:
                print(f"{row[0]:<20} | {row[1]:<25} | {row[2]}")