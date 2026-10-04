import os

from config import HTML_FILES,OUTPUT_CSV
from scraper import scrape_pages,deduplicate_records
from google_sheets import save_csv,upload_to_google_sheets




def main():

    records = scrape_pages(HTML_FILES)

    print(
        "\nTotal before deduplication:",
        len(records)
    )

    records = deduplicate_records(records)

    print(
        "Total after deduplication:",
        len(records)
    )

    # Create output folder if it doesn't exist
    output_folder = os.path.dirname(OUTPUT_CSV)

    if output_folder:
        os.makedirs(output_folder,exist_ok=True)

    save_csv(records,OUTPUT_CSV)

    sheet_url = upload_to_google_sheets(records)

    print("\nFinal Sheet:")
    print(sheet_url)
if __name__ == "__main__":
    main()