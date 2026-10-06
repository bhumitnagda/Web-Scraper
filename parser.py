from bs4 import BeautifulSoup


def extract_form_data(soup: BeautifulSoup) -> dict[str, str]:
    # extract enabled form controls for an ASP.NET postback.
    form = soup.find("form", {"id": "form1"}) or soup.find("form")
    if not form:
        return {}

    data = {}

    for inp in form.find_all("input"):
        if inp.has_attr("disabled"):
            continue

        name = inp.get("name")
        if not name:
            continue

        inp_type = inp.get("type", "text").lower()
        if inp_type in ["checkbox", "radio"]:
            if inp.has_attr("checked"):
                data[name] = inp.get("value", "on")
        elif inp_type not in ["submit", "image", "button"]:
            data[name] = inp.get("value", "")

    for select in form.find_all("select"):
        if select.has_attr("disabled"):
            continue

        name = select.get("name")
        if not name:
            continue

        selected_option = select.find("option", selected=True)
        if selected_option:
            data[name] = selected_option.get("value", "")
        else:
            first_option = select.find("option")
            data[name] = first_option.get("value", "") if first_option else ""

    return data


def parse_results_table(soup: BeautifulSoup) -> list[dict[str, str]]:
    # extracted the requested fields from the SearchIQS results table.
    records = []
    table = soup.find("table", {"id": "ContentPlaceHolder1_grdResults"})
    if not table:
        return records

    for row in table.find_all("tr")[1:]:
        cells = row.find_all("td")
        if len(cells) < 12:
            continue

        records.append(
            {
                "Party 1": cells[4].get_text(separator=" / ", strip=True),
                "Party 2": cells[5].get_text(separator=" / ", strip=True),
                "Type": cells[6].get_text(strip=True),
                "Book-Page": cells[7].get_text(strip=True),
                "Date": cells[8].get_text(strip=True),
                "Description": cells[9].get_text(strip=True),
                "Additional Description": cells[10].get_text(strip=True),
                "Related": cells[11].get_text(strip=True),
            }
        )

    return records
