"""
Genentech scraper
"""
from playwright.sync_api import sync_playwright
from datetime import datetime
import hashlib


def scrape_COMPANY_jobs():
    """
    Scrape jobs from [COMPANY NAME] careers page

    Returns:
        list: List of job dictionaries with structure:
              {
                  'job_id': str,      # MD5 hash of job URL
                  'title': str,       # Job title
                  'company': str,     # Company name
                  'location': str,    # Job location
                  'url': str,         # Job posting URL
                  'source': str,      # Source identifier
                  'status': str,      # 'active'
                  'first_seen': str,  # ISO timestamp
                  'last_seen': str    # ISO timestamp
              }
    """
    jobs = []

    # ============================================
    # CONFIGURATION - Update these for each company
    # ============================================
    url = "https://careers.gene.com/us/en"
    company_name = "Genentech"
    source_id = "genentech"

    # ============================================
    # STEP 1: Launch Browser & Navigate
    # ============================================
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True) #Can set headless to false when testing
        page = browser.new_page()
        page.goto(url, wait_until='networkidle')

        # ============================================
        # STEP 2: CUSTOM SCRAPING LOGIC
        # ============================================
        # TODO: Add your page-specific scraping logic here

        # page.click('input')
        # page.type('input', 'intern', delay=100)
        # page.press('input', 'Enter')
        # page.wait_for_load_state('networkidle')

        # Example template:
        # job_elements = page.query_selector_all('.job-listing')  # Update selector
        #
        # for element in job_elements:
        #     # Extract job information
        #     title = element.query_selector('.title').inner_text()  # Update selector
        #     location = element.query_selector('.location').inner_text()  # Update selector
        #     job_url = element.query_selector('a').get_attribute('href')  # Update selector
        #
        #     # Make URL absolute if needed
        #     if not job_url.startswith('http'):
        #         job_url = f"https://example.com{job_url}"
        #
        #     # STEP 3: Filter for internships/co-ops only
        #     if 'intern' in title.lower() or 'co-op' in title.lower():
        #
        #         # STEP 4: Create job dictionary
        #         job_id = hashlib.md5(job_url.encode()).hexdigest()
        #         timestamp = datetime.utcnow().isoformat()
        #
        #         job = {
        #             'job_id': job_id,
        #             'title': title,
        #             'company': company_name,
        #             'location': location,
        #             'url': job_url,
        #             'source': source_id,
        #             'status': 'active',
        #             'first_seen': timestamp,
        #             'last_seen': timestamp
        #         }
        #
        #         jobs.append(job)

        # ============================================
        # STEP 5: Cleanup
        # ============================================
        browser.close()

    return jobs


# For testing this scraper individually
if __name__ == "__main__":
    result = scrape_COMPANY_jobs()
    print(f"Found {len(result)} internship(s)")
    for job in result:
        print(f"  - {job['title']} at {job['location']}")
