"""
Cohere scraper
"""
from playwright.sync_api import sync_playwright
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

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True) #Keep True
        page = browser.new_page()
        page.goto(url, wait_until='networkidle')

        # Get all job listing elements
        job_elements = page.query_selector_all('div._departments_12ylk_345 > div > a > div')

        for element in job_elements:
            # print("element text_content:", element.text_content())
            # if "Intern" in element.text_content():
            # if re.search(r'\bIntern\b', element.text_content()):
            if re.search(r'\b(intern|internship)\b', element.text_content(), re.IGNORECASE):
                title = element.query_selector('h3').text_content()
                # print("Job title:", title)
                location = element.query_selector('div > p').text_content()
                # print("Job location:", location)
                # job_url = element.query_selector('div._departments_12ylk_345 > div > a').get_attribute('href')
                job_url = element.evaluate('el => el.parentElement.parentElement.querySelector("a").href')
                # if not job_url.startswith('http'):
                #     job_url = f"https://cohere.com{job_url}"
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
    result = scrape_cohere_jobs()
    print(f"Found {len(result)} internship(s)")
    for job in result:
        print(f"  - {job['title']} at {job['location']}")
