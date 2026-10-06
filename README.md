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

It also creates a Google Sheet, uploads the records, and prints the sheet URL.
Google OAuth credentials must be available in `credentials.json`; the first
successful login creates `authorized_user.json`.
