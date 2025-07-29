# portals/linkedin.py

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_linkedin(query: str, location: str, pages: int = 1) -> pd.DataFrame:
    jobs = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # set True in production
        page = browser.new_page()

        base_url = f"https://www.linkedin.com/jobs/search/?keywords={query.replace(' ', '%20')}&location={location.replace(' ', '%20')}&start="
        print(f"[LinkedIn] Launching scraper...")

        for page_num in range(pages):
            start = page_num * 25
            url = f"{base_url}{start}"
            print(f"[LinkedIn] Scraping page {page_num+1}: {url}")
            page.goto(url, timeout=60000)
            time.sleep(5)
            soup = BeautifulSoup(page.content(), "html.parser")

            for card in soup.select("li.jobs-search-results__list-item"):
                try:
                    title = card.find("span", class_="sr-only").get_text(strip=True)
                    company = card.find("h4").get_text(strip=True)
                    loc = card.find("span", class_="job-search-card__location").get_text(strip=True)
                    job_link = card.find("a", href=True)["href"]
                    jobs.append({
                        "Job Title": title,
                        "Company": company,
                        "Location": loc,
                        "Job Link": job_link
                    })
                except Exception as e:
                    print(f"⚠️ LinkedIn job parse error: {e}")

        browser.close()

    return pd.DataFrame(jobs)
