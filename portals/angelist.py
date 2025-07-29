# portals/angellist.py

import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_angellist(query: str, location: str, pages: int = 1) -> pd.DataFrame:
    jobs = []
    headers = {"User-Agent": "Mozilla/5.0"}

    for page in range(1, pages + 1):
        url = f"https://wellfound.com/jobs?keyword={query.replace(' ', '%20')}&location={location.replace(' ', '%20')}&page={page}"
        print(f"[AngelList] Scraping page {page}: {url}")

        try:
            res = requests.get(url, headers=headers)
            soup = BeautifulSoup(res.text, "html.parser")
            cards = soup.find_all("div", class_="styles_component__eGMmF")

            for card in cards:
                try:
                    title = card.find("div", class_="styles_title__J5pzb").get_text(strip=True)
                    company = card.find("div", class_="styles_name__FsXjN").get_text(strip=True)
                    loc = card.find("div", class_="styles_location__keAfP").get_text(strip=True)
                    job_link_tag = card.find("a", href=True)
                    job_link = "https://wellfound.com" + job_link_tag['href'] if job_link_tag else None

                    jobs.append({
                        "Job Title": title,
                        "Company": company,
                        "Location": loc,
                        "Job Link": job_link
                    })
                except Exception as e:
                    print(f"⚠️ Error parsing AngelList job card: {e}")
        except Exception as e:
            print(f"❌ Error loading AngelList page {page}: {e}")

    return pd.DataFrame(jobs)
