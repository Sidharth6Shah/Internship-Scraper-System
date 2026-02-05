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
        browser = p.chromium.launch(headless=True) #Keep True
        page = browser.new_page()
        page.goto(url, wait_until='networkidle')

        page.click('input')
        page.type('input', 'intern', delay=100)
        page.press('input', 'Enter')
        page.wait_for_load_state('networkidle')

        # Get all job listing elements
        job_elements = page.query_selector_all('ul > li')

        for element in job_elements:
            # Extract job information
            title = element.query_selector('h4').inner_text()
            location = element.query_selector('h5').inner_text()
            job_url = element.query_selector('a').get_attribute('href')

            # Make URL absolute if needed
            if not job_url.startswith('http'):
                job_url = f"https://neuralink.com{job_url}"

            # Create job dictionary
            job_id = hashlib.md5(job_url.encode()).hexdigest()
            timestamp = datetime.utcnow().isoformat()

            job = {
                'job_id': job_id,
                'title': title,
                'company': company_name,
                'location': location,
                'url': job_url,
                'source': source_id,
                'status': 'active',
                'first_seen': timestamp,
                'last_seen': timestamp
            }

            jobs.append(job)
            # print(f"Found: {title} - {location}")

        print(f"\nTotal jobs found: {len(jobs)}")
        time.sleep(5)  # Keep browser open for 5 seconds

        browser.close()

    return jobs


# For testing this scraper individually
if __name__ == "__main__":
    result = scrape_neuralink_jobs()
    # print(f"Found {len(result)} internship(s)")
    for job in result:
        print(f"  - {job['title']} at {job['location']}")
