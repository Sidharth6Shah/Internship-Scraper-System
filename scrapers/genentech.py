"""
Genentech scraper
"""
from playwright.sync_api import sync_playwright
from datetime import datetime
import hashlib


def scrape_genentech_jobs():
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
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until='networkidle')

        #Accept all popup
        if page.query_selector('#onetrust-accept-btn-handler'):
            page.click('#onetrust-accept-btn-handler')
            page.wait_for_timeout(1000)

        page.wait_for_selector('#typehead')
        page.click('#typehead')
        page.fill('#typehead', 'intern')
        page.press('#typehead', 'Enter')
        page.wait_for_load_state('networkidle')
        page.wait_for_selector('div.content-block.au-target.phw-content-block-nd > ul > li')
        
        #Scrape first page
        job_elements = page.query_selector_all('div.content-block.au-target.phw-content-block-nd > ul > li')
        for element in job_elements:
            title = element.query_selector('div > div > span > a > div > span').inner_text()
            location = element.query_selector('div > div > p > span > span').inner_text()
            job_url = element.query_selector('a').get_attribute('href')

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

        while True:
            nextButton = page.query_selector('li:nth-child(7) > a > span:nth-child(1) > ppc-content')
            if not nextButton:
                break
            parent_li = page.query_selector('li:nth-child(7)')
            if not nextButton.is_visible():
                break  # On the last page
            nextButton.click()
            page.wait_for_load_state('networkidle')
            page.wait_for_selector('div.content-block.au-target.phw-content-block-nd > ul > li')
            job_elements = page.query_selector_all('div.content-block.au-target.phw-content-block-nd > ul > li')
            for element in job_elements:
                title = element.query_selector('div > div > span > a > div > span').inner_text()
                location = element.query_selector('div > div > p > span > span').inner_text()
                job_url = "https://careers.gene.com/us/en"
                
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
        browser.close()
    return jobs


# For testing this scraper individually
if __name__ == "__main__":
    result = scrape_genentech_jobs()
    print(f"Found {len(result)} internship(s)")
    for job in result:
        print(f"  - {job['title']} at {job['location']}")
