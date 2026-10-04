from bs4 import BeautifulSoup
import re

def clean_text(cell) -> str:
    parts = []

    for text in cell.stripped_strings:
        trimmed = text.strip()

        if trimmed:
            parts.append(trimmed)

    return "\n".join(parts)


def parse_records(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find(
        "table",
        id="ContentPlaceHolder1_grdResults"
    )
    if not table:
        raise ValueError("Table not found")

    records = []

    rows = table.find_all("tr")[1:] # skip the header row

    for row in rows:
        cells = row.find_all("td")

        if len(cells) < 12:
            continue  # Skip rows having column less than 12

        record = {
                    "RecordID": clean_text(cells[3]),
                    "Party 1": clean_text(cells[4]),
                    "Party 2": clean_text(cells[5]),
                    "Type": clean_text(cells[6]),
                    "Book-Page": clean_text(cells[7]),
                    "Date": clean_text(cells[8]),
                    "Description": clean_text(cells[9]),
                    "Additional Description": clean_text(cells[10]),
                    "Related": clean_text(cells[11]),
                }
        records.append(record)

    return records