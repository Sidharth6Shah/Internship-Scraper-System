"""
Neuralink Scraper - Custom scraper for Neuralink job postings
"""
from playwright.sync_api import sync_playwright
from datetime import datetime
import hashlib
import time


def scrape_neuralink_jobs():
    """
    Scrape jobs from Neuralink careers page

    Returns:
        list: List of job dictionaries
    """
    jobs = []
    url = "https://neuralink.com/careers"
    company_name = "Neuralink"
    source_id = "neuralink"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False) #True
        page = browser.new_page()
        page.goto(url, wait_until='networkidle')

        # ============================================
        # TODO: Add your custom scraping logic here
        # ============================================
        # 1. Find job listing elements
        # 2. Loop through each element
        # 3. Extract: title, location, job_url
        # 4. Filter for internships/co-ops only
        # 5. Create job dictionary and append to jobs list

        print("Browser opened - check your screen!")
        time.sleep(10)  # Keep browser open for 10 seconds

        browser.close()

    return jobs


# For testing this scraper individually
if __name__ == "__main__":
    result = scrape_neuralink_jobs()
    print(f"Found {len(result)} internship(s)")
    for job in result:
        print(f"  - {job['title']} at {job['location']}")
