# app.py

import streamlit as st
import pandas as pd

from portals import naukri, internshala, indeed, cutshort, angelist, linkedin

st.set_page_config(page_title="🔍 Job Aggregator", layout="wide")
st.title("📊 Multi-Portal Job Search Aggregator")

# --- Sidebar Inputs ---
st.sidebar.header("🔧 Search Filters")
query = st.sidebar.text_input("Job Role", value="Python Developer")
location = st.sidebar.text_input("Location", value="Bhubaneswar")
experience = st.sidebar.selectbox("Experience", ["0-1 years", "1-3 years", "3-5 years", "5+ years"])
pages = st.sidebar.slider("Pages to Scrape (per portal)", 1, 5, 2)
selected_portals = st.sidebar.multiselect(
    "Select Portals",
    ["Naukri", "Internshala", "Indeed", "CutShort", "AngelList", "LinkedIn"],
    default=["Naukri", "Internshala"]
)

# --- Scrape & Show ---
if st.button("🚀 Search Jobs"):
    st.info("Scraping jobs... please wait")
    all_jobs = []

    with st.spinner("Scraping selected portals..."):
        progress = st.progress(0)
        total = len(selected_portals)

        for idx, portal in enumerate(selected_portals):
            if portal == "Naukri":
                st.write("🔸 Scraping Naukri...")
                df = naukri.scrape_naukri(query, location, pages)
                df["Portal"] = "Naukri"
                all_jobs.append(df)

            elif portal == "Internshala":
                st.write("🔹 Scraping Internshala...")
                df = internshala.scrape_internshala(query, location, pages)
                df["Portal"] = "Internshala"
                all_jobs.append(df)

            elif portal == "Indeed":
                st.write("⚪ Scraping Indeed...")
                df = indeed.scrape_indeed(query, location, pages)
                df["Portal"] = "Indeed"
                all_jobs.append(df)

            elif portal == "CutShort":
                st.write("🟣 Scraping CutShort...")
                df = cutshort.scrape_cutshort(query, location, pages)
                df["Portal"] = "CutShort"
                all_jobs.append(df)

            elif portal == "AngelList":
                st.write("🟤 Scraping AngelList...")
                df = angelist.scrape_angelist(query, location, pages)
                df["Portal"] = "AngelList"
                all_jobs.append(df)

            elif portal == "LinkedIn":
                st.write("🔷 Scraping LinkedIn...")
                df = linkedin.scrape_linkedin(query, location, pages)
                df["Portal"] = "LinkedIn"
                all_jobs.append(df)

            progress.progress((idx + 1) / total)

    # Combine results
    if all_jobs:
        final_df = pd.concat(all_jobs, ignore_index=True)
        st.success(f"✅ Found {len(final_df)} jobs from {len(selected_portals)} portal(s)")
        st.dataframe(final_df)

        csv = final_df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download Results as CSV", data=csv, file_name="jobs.csv", mime="text/csv")
    else:
        st.warning("No jobs found or portals were empty.")
