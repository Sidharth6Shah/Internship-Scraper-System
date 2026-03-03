"""
AstraZeneca Scraper - Custom scraper for AstraZeneca job postings
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
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

    chrome_options = Options()
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--single-process')
    chrome_options.add_argument('--disable-dev-tools')
    chrome_options.add_argument('--no-zygote')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36')
    chrome_options.binary_location = '/opt/chrome/chrome-linux64/chrome'

    driver = webdriver.Chrome(
        options=chrome_options,
        service=webdriver.ChromeService(executable_path='/opt/chromedriver')
    )

    try:
        driver.get(url)
        time.sleep(3)

        # Close cookie banner
        try:
            cookie_btn = driver.find_element(By.CSS_SELECTOR, 'a.wscrOk')
            cookie_btn.click()
        except:
            print("Cookie banner not found, continuing...")

        # Click form toggle
        try:
            toggle = driver.find_element(By.CSS_SELECTOR, 'div.form-toggle-button-container > div > div > span')
            toggle.click()
            time.sleep(1)
        except:
            print("Form toggle not found, continuing...")

        # Search for intern
        try:
            wait = WebDriverWait(driver, 10)
            # Clear location filter
            location_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div > p:nth-child(2) > input')))
            location_input.click()
            location_input.clear()
            time.sleep(0.5)

            # Type intern in search
            keyword_input = driver.find_element(By.CSS_SELECTOR, 'div > p:nth-child(1) > input')
            keyword_input.click()
            keyword_input.send_keys('intern')
            keyword_input.submit()

            # Wait for results
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#search-results-list > ul > li')))
            time.sleep(2)
        except Exception as e:
            print(f"Error during search: {e}")
            return jobs

        # Get all job listing elements
        job_elements = driver.find_elements(By.CSS_SELECTOR, '#search-results-list > ul > li')

        for element in job_elements:
            try:
                title = element.find_element(By.CSS_SELECTOR, 'a > div:nth-child(2) > h2').text
                location = element.find_element(By.CSS_SELECTOR, 'a > div:nth-child(2) > span').text
                job_url = element.find_element(By.TAG_NAME, 'a').get_attribute('href')

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
            except Exception as e:
                print(f"Error extracting job: {e}")
                continue

        print(f"\nTotal jobs found: {len(jobs)}")

    finally:
        driver.quit()

    return jobs


# For testing this scraper individually
if __name__ == "__main__":
    result = scrape_astrazeneca_jobs()
    for job in result:
        print(f"  - {job['title']} at {job['location']}")
