"""
AstraZeneca Scraper - Custom scraper for AstraZeneca job postings
"""
from playwright.sync_api import sync_playwright
from datetime import datetime
import hashlib
import time


def scrape_astrazeneca_jobs():
    """
    Scrape jobs from AstraZeneca careers page

    Returns:
        list: List of job dictionaries
    """
    jobs = []
    url = "https://careers.astrazeneca.com/canada"
    company_name = "Astrazeneca"
    source_id = "astrazeneca"

    with sync_playwright() as p:
        # browser = p.chromium.launch(headless=True) #Keep True
        # page = browser.new_page()
        browser = p.chromium.launch(
            headless=True,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox'
            ]
        )
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        )
        page = context.new_page()


        # Try with a longer timeout and different wait strategy
        try:
            page.goto(url, timeout=60000, wait_until='domcontentloaded')
            page.wait_for_timeout(3000)  # Wait 3 seconds for dynamic content
        except Exception as e:
            print(f"Error loading page: {e}")
            browser.close()
            return jobs

        try:
            page.click('a.wscrOk', timeout=5000)
        except:
            print("Cookie banner not found, continuing...")

        try:
            page.click('div.form-toggle-button-container > div > div > span', timeout=5000)
            page.wait_for_timeout(1000)
        except:
            print("Form toggle not found, continuing...")

        try:
            page.wait_for_selector('div > p:nth-child(2) > input', timeout=10000)
            page.click('div > p:nth-child(2) > input')
            page.fill('input', '')
            page.wait_for_timeout(500)

            page.click('div > p:nth-child(1) > input')
            page.type('input', 'intern', delay=50)
            page.press('input', 'Enter')
            # page.click('#pagination-bottom > div.pagination-all > a') #Show all button

            # Wait longer for results in headless mode
            page.wait_for_selector('#search-results-list > ul > li', timeout=120000)
            page.wait_for_timeout(2000)  # Extra wait for all results to load
        except Exception as e:
            print(f"Error during search: {e}")
            browser.close()
            return jobs

        # Get all job listing elements
        job_elements = page.query_selector_all('#search-results-list > ul > li')

        for element in job_elements:
            # Extract job information
            title = element.query_selector('a > div:nth-child(2) > h2').inner_text()
            location = element.query_selector('a > div:nth-child(2) > span').inner_text()
            job_url = element.query_selector('a').get_attribute('href')

            # Make URL absolute if needed
            if not job_url.startswith('http'):
                job_url = f"https://careers.astrazeneca.com/{job_url}"

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
    result = scrape_astrazeneca_jobs()
    # print(f"Found {len(result)} internship(s)")
    for job in result:
        print(f"  - {job['title']} at {job['location']}")
