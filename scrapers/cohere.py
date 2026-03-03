"""
Cohere scraper
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import hashlib
import time
import re


def scrape_cohere_jobs():
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
    url = "https://jobs.ashbyhq.com/cohere"
    company_name = "Cohere"
    source_id = "cohere"

    # Chrome options for Lambda
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
        time.sleep(3)  # Wait for page to load

        # Get all job listing elements
        job_elements = driver.find_elements(By.CSS_SELECTOR, 'div._departments_12ylk_345 > div > a > div')

        for element in job_elements:
            try:
                element_text = element.text
                if re.search(r'\b(intern|internship)\b', element_text, re.IGNORECASE):
                    title = element.find_element(By.TAG_NAME, 'h3').text
                    location = element.find_element(By.CSS_SELECTOR, 'div > p').text
                    job_url = driver.execute_script(
                        'return arguments[0].parentElement.parentElement.querySelector("a").href',
                        element
                    )

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
            except Exception as e:
                print(f"Error extracting job: {e}")
                continue

        print(f"\nTotal jobs found: {len(jobs)}")

    finally:
        driver.quit()

    return jobs


# For testing this scraper individually
if __name__ == "__main__":
    result = scrape_cohere_jobs()
    print(f"Found {len(result)} internship(s)")
    for job in result:
        print(f"  - {job['title']} at {job['location']}")
