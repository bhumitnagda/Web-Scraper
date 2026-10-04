import csv
import gspread

FIELDNAMES = [
    "RecordID",
    "Party 1",
    "Party 2",
    "Type",
    "Book-Page",
    "Date",
    "Description",
    "Additional Description",
    "Related",
]


def save_csv(records: list[dict], filename: str) -> None:
    with open(
        filename,
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=FIELDNAMES
        )

        writer.writeheader()
        writer.writerows(records)

    print(f"saved {filename}")


SHEET_FIELDNAMES = [
    "Party 1",
    "Party 2",
    "Type",
    "Book-Page",
    "Date",
    "Description",
    "Additional Description",
    "Related",
]

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

def upload_to_google_sheets(records: list[dict]) -> str:
    # login to sheets using service account

    client = gspread.oauth(
    credentials_filename="credentials.json",
    authorized_user_filename="authorized_user.json",
    scopes=SCOPES,
)
    # create a spread sheet
    spreadsheet = client.create(
        "SearchIQS Ashford Land Records"
    )

    worksheet = spreadsheet.sheet1

    worksheet.update_title(
        "Land Records"
    )

    # first row is the header
    values = [
        SHEET_FIELDNAMES
    ]

    
    for record in records:

        row = []

        for field in SHEET_FIELDNAMES:
            row.append(
                record.get(field, "")
            )

        values.append(row)

    # upload in 1 go
    worksheet.update(
        values=values,
        range_name="A1"
    )

    #create a link to share the sheet
    spreadsheet.share(
        None,
        perm_type="anyone",
        role="reader",
        with_link=True,
        notify=False
    )

    print(
        "created google sheet"
    )

    print(
        "Google Sheet URL:",
        spreadsheet.url
    )

    return spreadsheet.url
