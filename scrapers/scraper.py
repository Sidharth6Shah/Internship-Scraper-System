"""
TEMPLATE SCRAPER - Duplicate this file for each company

Instructions:
1. Copy this file and rename it (e.g., anthropic.py, openai.py)
2. Update the function name to match company (e.g., scrape_anthropic_jobs)
3. Update url, company_name, and source_id
4. Fill in custom scraping logic in STEP 2
5. Add the scraper to config.py JOB_SOURCES
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
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
    url = "https://example.com/careers"
    company_name = "Company Name"
    source_id = "company_identifier"

    # ============================================
    # STEP 1: Launch Browser & Navigate
    # ============================================
    chrome_options = Options()
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--single-process')
    chrome_options.add_argument('--disable-dev-tools')
    chrome_options.add_argument('--no-zygote')
    chrome_options.binary_location = '/opt/chrome/chrome-linux64/chrome'

    driver = webdriver.Chrome(
        options=chrome_options,
        service=webdriver.ChromeService(executable_path='/opt/chromedriver')
    )

    try:
        driver.get(url)

        # ============================================
        # STEP 2: CUSTOM SCRAPING LOGIC
        # ============================================
        # TODO: Add your page-specific scraping logic here

        # Example: Get all job listing elements
        # job_elements = driver.find_elements(By.CSS_SELECTOR, 'ul > li')

        # for element in job_elements:
        #     try:
        #         title = element.find_element(By.TAG_NAME, 'h4').text
        #         location = element.find_element(By.TAG_NAME, 'h5').text
        #         job_url = element.find_element(By.TAG_NAME, 'a').get_attribute('href')
        #
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
        #     except Exception as e:
        #         print(f"Error extracting job: {e}")
        #         continue

        print(f"\nTotal jobs found: {len(jobs)}")

    finally:
        driver.quit()

    return jobs


# For testing this scraper individually
if __name__ == "__main__":
    result = scrape_COMPANY_jobs()
    print(f"Found {len(result)} internship(s)")
    for job in result:
        print(f"  - {job['title']} at {job['location']}")
