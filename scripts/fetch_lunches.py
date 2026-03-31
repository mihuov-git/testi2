import json
import re
from datetime import datetime
from pathlib import Path

import requests
from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
OUTPUT_FILE = DATA_DIR / "lunches.json"


HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; LunchBot/1.0)"
}


def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text or "").strip()
    return text


def fetch_grill_it():
    url = "https://www.raflaamo.fi/fi/ravintola/turku/grill-it-marina-turku/menu/lounas"
    items = []

    try:
        r = requests.get(url, headers=HEADERS, timeout=30)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "lxml")

        text_blocks = soup.find_all(["p", "li", "h2", "h3", "div"])
        texts = [clean_text(x.get_text(" ", strip=True)) for x in text_blocks]
        texts = [t for t in texts if t]

        start_idx = None
        for i, t in enumerate(texts):
            if "lounas" in t.lower():
                start_idx = i
                break

        if start_idx is not None:
            for t in texts[start_idx + 1:start_idx + 25]:
                low = t.lower()
                if any(stop in low for stop in ["à la carte", "juomat", "viinit", "cocktail", "yhteystiedot"]):
                    break
                if len(t) > 4 and t not in items:
                    items.append(t)

        if not items:
            items = ["Lounasta ei saatu haettua tällä hetkellä."]
    except Exception as e:
        items = [f"Lounaan haku epäonnistui: {type(e).__name__}"]

    return {
        "name": "Grill it! Marina",
        "url": url,
        "items": items,
    }


def fetch_fontana():
    url = "https://www.lounaat.info/lounas/fontana/turku"
    items = []

    try:
        r = requests.get(url, headers=HEADERS, timeout=30)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "lxml")

        selectors = [
            ".menu-item",
            ".dish",
            ".menu-content li",
            ".menu li",
            "article li",
            "main li",
        ]

        for selector in selectors:
            found = [clean_text(x.get_text(" ", strip=True)) for x in soup.select(selector)]
            found = [x for x in found if x]
            if found:
                items = found
                break

        if not items:
            all_li = [clean_text(x.get_text(" ", strip=True)) for x in soup.find_all("li")]
            items = [x for x in all_li if len(x) > 4][:20]

        if not items:
            items = ["Lounasta ei saatu haettua tällä hetkellä."]
    except Exception as e:
        items = [f"Lounaan haku epäonnistui: {type(e).__name__}"]

    return {
        "name": "Fontana",
        "url": url,
        "items": items,
    }


def fetch_tintti():
    url = "https://www.lounaat.info/lounas/ravintola-tintti/turku"
    items = []

    try:
        r = requests.get(url, headers=HEADERS, timeout=30)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "lxml")

        selectors = [
            ".menu-item",
            ".dish",
            ".menu-content li",
            ".menu li",
            "article li",
            "main li",
        ]

        for selector in selectors:
            found = [clean_text(x.get_text(" ", strip=True)) for x in soup.select(selector)]
            found = [x for x in found if x]
            if found:
                items = found
                break

        if not items:
            all_li = [clean_text(x.get_text(" ", strip=True)) for x in soup.find_all("li")]
            items = [x for x in all_li if len(x) > 4][:20]

        if not items:
            items = ["Lounasta ei saatu haettua tällä hetkellä."]
    except Exception as e:
        items = [f"Lounaan haku epäonnistui: {type(e).__name__}"]

    return {
        "name": "Tintti",
        "url": url,
        "items": items,
    }


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    data = {
        "updated_at": datetime.utcnow().isoformat() + "Z",
        "restaurants": [
            fetch_fontana(),
            fetch_tintti(),
            fetch_grill_it(),
        ],
    }

    OUTPUT_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"Wrote {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
