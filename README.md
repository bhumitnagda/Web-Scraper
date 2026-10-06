# SearchIQS Land Records Scraper

Scrapes the Connecticut SearchIQS Land Records results for the most recent 80
days, saves the records to CSV, and uploads them to a shareable Google Sheet.

## Setup

Create and activate a virtual environment, then install the dependencies:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Add your Cloudflare clearance cookie to the root `.env` file:

```text
CF_COOKIE=your_cf_clearance_cookie
```

The `.env` file is ignored by Git. Keep the cookie private and refresh it when
it expires.

## Run

```powershell
python main.py
```

The scraper follows the guest login and Land Records search flow, retrieves all
result pages, writes the eight extracted fields to:

```text
output/ashford_records.csv
```
<<<<<<< HEAD
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


=======
>>>>>>> 34bb97f (Updated code)

It also creates a Google Sheet, uploads the records, and prints the sheet URL.
Google OAuth credentials must be available in `credentials.json`; the first
successful login creates `authorized_user.json`.
