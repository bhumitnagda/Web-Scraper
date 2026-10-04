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
Google OAuth is used to create and update Google Sheets.

### 1. Create a Google Cloud Project

Go to Google Cloud Console and create a new project.

### 2. Enable Required APIs

Enable both:

- Google Sheets API
- Google Drive API

The Sheets API writes data to the spreadsheet, while the Drive API creates and shares the spreadsheet.

### 3. Configure OAuth

Open **Google Auth Platform** and configure the OAuth consent screen.

For development/testing:

- Select **External**
- Add your Google account as a **Test User**
- Add access for Google Sheets and Google Drive

### 4. Create OAuth Credentials

Go to:

**APIs & Services → Credentials → Create Credentials → OAuth Client ID**

Choose:

**Application type: Desktop app**

Download the generated JSON file and rename it to:
```text
credentials.json
```
The first successful login creates:
```text
authorized_user.json
```



