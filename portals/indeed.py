# portals/indeed.py

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_indeed(query: str, location: str, pages: int = 1) -> pd.DataFrame:
    jobs = []
    headers = {"User-Agent": "Mozilla/5.0"}

    for page in range(pages):
        start = page * 10
        url = (
            f"https://in.indeed.com/jobs?q={query.replace(' ', '+')}"
            f"&l={location.replace(' ', '+')}&start={start}"
        )

        print(f"[Indeed] Scraping page {page+1}: {url}")
        try:
            response = requests.get(url, headers=headers, timeout=20)
            soup = BeautifulSoup(response.text, "html.parser")

            cards = soup.find_all("div", class_="job_seen_beacon")
            for card in cards:
                try:
                    title = card.find("h2", {"class": "jobTitle"}).get_text(strip=True)
                    company = card.find("span", class_="companyName").get_text(strip=True)
                    loc = card.find("div", class_="companyLocation").get_text(strip=True)
                    summary_tag = card.find("div", class_="job-snippet")
                    summary = summary_tag.get_text(" ", strip=True) if summary_tag else None
                    salary_tag = card.find("div", class_="salary-snippet")
                    salary = salary_tag.get_text(strip=True) if salary_tag else "Not listed"
                    link_tag = card.find("a", href=True)
                    job_link = "https://in.indeed.com" + link_tag["href"] if link_tag else None

                    jobs.append({
                        "Job Title": title,
                        "Company": company,
                        "Location": loc,
                        "Summary": summary,
                        "Salary": salary,
                        "Job Link": job_link
                    })
                except Exception as inner_err:
                    print(f"⚠️ Error parsing a job card: {inner_err}")
        except Exception as req_err:
            print(f"❌ Failed to fetch Indeed page {page+1}: {req_err}")

        time.sleep(1)  # be polite

    return pd.DataFrame(jobs)
