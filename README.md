# SearchIQS Land Records Scraper

Python scraper for extracting land record data from manually saved SearchIQS result pages and exporting the results to CSV / Google Sheets.

## Features

- Parses multiple SearchIQS result pages
- Extracts:
  - Party 1
  - Party 2
  - Type
  - Book-Page
  - Date
  - Description
  - Additional Description
  - Related
- Removes duplicate records using RecordID
- Exports records to CSV
- Supports Google Sheets upload using OAuth

## Project Structure

```text
Web-Scraper/
├── main.py
├── parser.py
├── scraper.py
├── google_sheets.py
├── config.py
├── requirements.txt
└── .gitignore
```
## Setup
Create and activate a virtual environment in the terminal:
```bash
python -m venv venv
venv\Scripts\activate
```
Install dependencies:
```text
pip install -r requirements.txt
```
Place the manually downloaded SearchIQS result pages in the project folder.
Example:
```
Search Results.html
```
Run:
```text
python main.py
```
The script will:

- Parse all configured HTML pages
- Combine the extracted records
- Remove duplicate records and save the result to:
```text
output/ashford_records.csv
```
## Google Sheets Setup
Download a Google OAuth Desktop Client JSON file and save it as:
```text
credentials.json
```
The first successful login creates:
```text
authorized_user.json
```



