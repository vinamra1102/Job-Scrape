# portals/cutshort.py

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_cutshort(query: str, location: str, pages: int = 1) -> pd.DataFrame:
    jobs = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        base_url = f"https://cutshort.io/jobs/{query.replace(' ', '-')}-jobs-in-{location.replace(' ', '-')}"
        print(f"[CutShort] Scraping: {base_url}")
        page.goto(base_url)
        time.sleep(5)
        soup = BeautifulSoup(page.content(), "html.parser")

        cards = soup.find_all("div", class_="job-listing-wrapper")
        for card in cards:
            try:
                title = card.find("h2").get_text(strip=True)
                company = card.find("div", class_="company-name-text").get_text(strip=True)
                job_url_tag = card.find("a", href=True)
                job_url = "https://cutshort.io" + job_url_tag['href'] if job_url_tag else None
                location_tag = card.find("div", class_="location-text")
                loc = location_tag.get_text(strip=True) if location_tag else "Remote / Flexible"

                jobs.append({
                    "Job Title": title,
                    "Company": company,
                    "Location": loc,
                    "Job Link": job_url
                })
            except Exception as e:
                print(f"⚠️ Error parsing CutShort job card: {e}")

        browser.close()

    return pd.DataFrame(jobs)
