from parser import parse_records


def load_html(path):
    with open(
        path,
        "r",
        encoding="utf-8",
        errors="ignore"
    ) as f:
        return f.read()

def scrape_pages(paths):
    all_records = []

    for path in paths: 
        html = load_html(path)
        records = parse_records(html)
        print(
            f"{path}: {len(records)} records"
        )

        all_records.extend(records)

    return all_records

def deduplicate_records(records):
    seen = set()
    unique = []

    for record in records: # record is dictionary from parse_records function
        record_id = record["RecordID"]

        if record_id not in seen:
            seen.add(record_id)
            unique.append(record)

    return unique

