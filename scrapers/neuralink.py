"""
Neuralink Scraper - Custom scraper for Neuralink job postings
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import hashlib
import time
import os


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

    # Set up Chrome driver
    driver = webdriver.Chrome(
        options=chrome_options,
        service=webdriver.ChromeService(executable_path='/opt/chromedriver')
    )

    try:
        driver.get(url)

        # Wait for page to load and find input
        wait = WebDriverWait(driver, 10)
        input_elem = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'input')))

        # Type in search and press Enter
        input_elem.click()
        input_elem.send_keys('intern')
        from selenium.webdriver.common.keys import Keys
        input_elem.send_keys(Keys.RETURN)

        # Wait for results
        time.sleep(3)

        # Get all job listing elements
        job_elements = driver.find_elements(By.CSS_SELECTOR, 'ul > li')

        for element in job_elements:
            try:
                # Extract job information
                title = element.find_element(By.TAG_NAME, 'h4').text
                location = element.find_element(By.TAG_NAME, 'h5').text
                job_url = element.find_element(By.TAG_NAME, 'a').get_attribute('href')

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
            except Exception as e:
                print(f"Error extracting job: {e}")
                continue

        print(f"\nTotal jobs found: {len(jobs)}")

    finally:
        driver.quit()

    return jobs


# For testing this scraper individually
if __name__ == "__main__":
    result = scrape_neuralink_jobs()
    for job in result:
        print(f"  - {job['title']} at {job['location']}")
