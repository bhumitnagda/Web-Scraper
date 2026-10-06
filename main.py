import os

from dotenv import load_dotenv

from config import OUTPUT_CSV
from google_sheets import save_csv, upload_to_google_sheets
from scraper import run_scraper


def main():
    load_dotenv()
    cf_cookie = os.getenv("CF_COOKIE", "").strip()
    if not cf_cookie:
        raise RuntimeError(
            "CF_COOKIE is not set."
        )

    records = run_scraper(cf_clearance_cookie=cf_cookie)
    if not records:
        print("No records to save.")
        return

    output_folder = os.path.dirname(OUTPUT_CSV)
    if output_folder:
        os.makedirs(output_folder, exist_ok=True)

    save_csv(records, OUTPUT_CSV)
    sheet_url = upload_to_google_sheets(records)
    print("\nFinal Sheet:")
    print(sheet_url)

if __name__ == "__main__":
    main()