from datetime import datetime, timedelta

from bs4 import BeautifulSoup
from curl_cffi import requests

from parser import extract_form_data, parse_results_table

BASE_URL = "https://www.searchiqs.com/CTASH"


def run_scraper(cf_clearance_cookie: str | None = None) -> list[dict[str, str]]:
    today = datetime.now()
    from_date = (today - timedelta(days=80)).strftime("%m/%d/%Y")
    to_date = today.strftime("%m/%d/%Y")

    print(f"Target Date Range: {from_date} to {to_date}")

    session = requests.Session(impersonate="chrome120")
    session.headers.update(
        {
            "Accept": (
                "text/html,application/xhtml+xml,application/xml;q=0.9,"
                "image/avif,image/webp,image/apng,*/*;q=0.8"
            ),
            "Accept-Language": "en-US,en;q=0.9",
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/153.0.0.0 Safari/537.36"
            ),
        }
    )

    if cf_clearance_cookie:
        session.cookies.set(
            "cf_clearance",
            cf_clearance_cookie,
            domain=".searchiqs.com",
        )

    print("[1/5] Loading landing page...")
    response = session.get(f"{BASE_URL}/")
    print(f"-> Status: {response.status_code}, URL: {response.url}")
    if response.status_code != 200:
        print("Blocked by Cloudflare on initial request.")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    print("[2/5] Submitting guest login...")
    payload = extract_form_data(soup)
    payload["__EVENTTARGET"] = "btnGuestLogin"
    payload["__EVENTARGUMENT"] = ""
    payload["BrowserWidth"] = "1240"
    payload["BrowserHeight"] = "762"

    headers_post = {
        "Origin": "https://www.searchiqs.com",
        "Referer": f"{BASE_URL}/",
    }
    response = session.post(
        f"{BASE_URL}/",
        data=payload,
        headers=headers_post,
        allow_redirects=True,
    )
    print(f"-> Status: {response.status_code}, URL: {response.url}")

    if "SearchAdvancedMP.aspx" not in response.url:
        response = session.get(f"{BASE_URL}/SearchAdvancedMP.aspx")
        print(f"-> Navigated to: {response.url}")

    soup = BeautifulSoup(response.text, "html.parser")

    print("[3/5] Setting document group to Land Records...")
    payload = extract_form_data(soup)
    payload["__EVENTTARGET"] = "ctl00$ContentPlaceHolder1$cboDocGroup"
    payload["__EVENTARGUMENT"] = ""
    payload["ctl00$ContentPlaceHolder1$cboDocGroup"] = "LR"
    payload["ctl00$ContentPlaceHolder1$chkIgnorePartyType"] = "on"
    payload["BrowserWidth"] = "1240"
    payload["BrowserHeight"] = "762"

    headers_post["Referer"] = f"{BASE_URL}/SearchAdvancedMP.aspx"
    response = session.post(
        f"{BASE_URL}/SearchAdvancedMP.aspx",
        data=payload,
        headers=headers_post,
        allow_redirects=True,
    )
    print(f"-> Status: {response.status_code}, URL: {response.url}")
    soup = BeautifulSoup(response.text, "html.parser")

    print(f"[4/5] Executing search for {from_date} -> {to_date}...")
    payload = extract_form_data(soup)
    payload["__EVENTTARGET"] = ""
    payload["__EVENTARGUMENT"] = ""
    payload["ctl00$ContentPlaceHolder1$cboDocGroup"] = "LR"
    payload["ctl00$ContentPlaceHolder1$cboDocType"] = "(ALL)"
    payload["ctl00$ContentPlaceHolder1$txtFromDate"] = from_date
    payload["ctl00$ContentPlaceHolder1$txtThruDate"] = to_date
    payload["ctl00$ContentPlaceHolder1$chkIgnorePartyType"] = "on"
    payload["ctl00$ContentPlaceHolder1$cmdSearch"] = "Search"
    payload["BrowserWidth"] = "1240"
    payload["BrowserHeight"] = "762"

    response = session.post(
        f"{BASE_URL}/SearchAdvancedMP.aspx",
        data=payload,
        headers=headers_post,
        allow_redirects=True,
    )
    print(f"-> Status: {response.status_code}, URL: {response.url}")
    soup = BeautifulSoup(response.text, "html.parser")

    if "SearchResultsMP.aspx" not in response.url:
        error_tag = soup.find("span", {"id": "ContentPlaceHolder1_lblGeneralError"})
        error_message = error_tag.get_text(strip=True) if error_tag else "None"
        print("[!] Warning: Did not redirect to SearchResultsMP.aspx.")
        print(f"[!] Server Error Message: {error_message}")
        return []

    count_tag = soup.find(
        "span", {"id": "ContentPlaceHolder1_lblSearchResults"}
    ) or soup.find("span", {"id": "ContentPlaceHolder1_lblSearchCount"})
    if count_tag:
        print(f"Search summary: {count_tag.get_text(strip=True)}")

    print("[5/5] Extracting records...")
    all_records = []
    page = 1

    while True:
        records = parse_results_table(soup)
        all_records.extend(records)
        print(
            f"-> Page {page}: Scraped {len(records)} records "
            f"(Cumulative: {len(all_records)})"
        )

        next_link = soup.find("a", {"id": "ContentPlaceHolder1_lbNext1"})
        if not next_link or "aspNetDisabled" in next_link.get("class", []):
            print("Reached final page.")
            break

        payload = extract_form_data(soup)
        payload["__EVENTTARGET"] = "ctl00$ContentPlaceHolder1$lbNext1"
        payload["__EVENTARGUMENT"] = ""
        payload["ctl00$ContentPlaceHolder1$ddlSource"] = "Search Results"

        headers_post["Referer"] = f"{BASE_URL}/SearchResultsMP.aspx"
        response = session.post(
            f"{BASE_URL}/SearchResultsMP.aspx",
            data=payload,
            headers=headers_post,
            allow_redirects=True,
        )
        soup = BeautifulSoup(response.text, "html.parser")
        page += 1

    return all_records
