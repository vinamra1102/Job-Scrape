# portals/naukri.py

from bs4 import BeautifulSoup
import pandas as pd
import time
from utils.browser import BrowserManager

def scrape_naukri(query: str, location: str, pages: int = 1) -> pd.DataFrame:
    jobs = []
    with BrowserManager() as page:
        for i in range(pages):
            start = i * 20
            url = f"https://www.naukri.com/{query.replace(' ', '-')}-jobs-in-{location.replace(' ', '-')}-{start}?k={query}&l={location}&start={start}"
            print(f"[Naukri] Scraping: {url}")
            page.goto(url, timeout=60000)
            time.sleep(3)
            soup = BeautifulSoup(page.content(), "html.parser")

            for card in soup.find_all("article", class_="jobTuple"):
                try:
                    title = card.find("a", class_="title").get_text(strip=True)
                    company = card.find("a", class_="subTitle").get_text(strip=True)
                    location_tag = card.find("li", class_="location")
                    experience_tag = card.find("li", class_="experience")
                    skills_tag = card.find("ul", class_="tags")
                    job_link = card.find("a", class_="title")["href"]

                    jobs.append({
                        "Job Title": title,
                        "Company": company,
                        "Location": location_tag.get_text(strip=True) if location_tag else None,
                        "Experience": experience_tag.get_text(strip=True) if experience_tag else None,
                        "Skills": skills_tag.get_text(" | ", strip=True) if skills_tag else None,
                        "Job Link": job_link
                    })
                except Exception as e:
                    print(f"⚠️ Error parsing Naukri job card: {e}")
    return pd.DataFrame(jobs)
