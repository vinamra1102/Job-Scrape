# portals/internshala.py

import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_internshala(query, location, pages=1):
    base_url = "https://internshala.com/internships"
    results = []

    for page in range(1, pages + 1):
        query_slug = query.lower().replace(" ", "-")
        location_slug = location.lower().replace(" ", "-")
        url = f"{base_url}/{query_slug}-internship-in-{location_slug}/page-{page}"
        print(f"[Internshala] Scraping: {url}")

        try:
            res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
            soup = BeautifulSoup(res.text, "html.parser")
            job_cards = soup.find_all("div", class_="internship_meta")

            for card in job_cards:
                try:
                    container = card.find_parent("div", class_="individual_internship")
                    if not container:
                        continue

                    title = container.find("div", class_="heading_4_5").get_text(strip=True) if container.find("div", class_="heading_4_5") else "N/A"
                    company = container.find("a", class_="link_display_like_text").get_text(strip=True) if container.find("a", class_="link_display_like_text") else "N/A"
                    location = container.find("a", class_="location_link").get_text(strip=True) if container.find("a", class_="location_link") else "N/A"
                    start_date = container.select_one("div.start-date div.item_body")
                    duration = container.select_one("div.duration div.item_body")
                    stipend = container.select_one("div.stipend div.item_body")
                    link_tag = container.find("a", class_="view_detail_button")

                    job_data = {
                        "Job Title": title,
                        "Company": company,
                        "Location": location,
                        "Start Date": start_date.get_text(strip=True) if start_date else "N/A",
                        "Duration": duration.get_text(strip=True) if duration else "N/A",
                        "Stipend": stipend.get_text(strip=True) if stipend else "N/A",
                        "Job Link": "https://internshala.com" + link_tag["href"] if link_tag and link_tag.get("href") else "N/A",
                        "Portal": "Internshala"
                    }

                    results.append(job_data)

                except Exception as e:
                    print("⚠️ Error parsing job:", e)
                    continue

        except Exception as e:
            print("❌ Error loading Internshala page:", e)
            continue

    df = pd.DataFrame(results)
    return df
