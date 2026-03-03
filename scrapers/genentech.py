"""
Genentech scraper
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import hashlib
import time


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
        wait = WebDriverWait(driver, 10)

        # Accept cookie popup if present
        try:
            accept_btn = driver.find_element(By.ID, 'onetrust-accept-btn-handler')
            accept_btn.click()
            time.sleep(1)
        except:
            pass

        # Search for intern
        search_box = wait.until(EC.presence_of_element_located((By.ID, 'typehead')))
        search_box.click()
        search_box.send_keys('intern')
        search_box.submit()

        time.sleep(3)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.content-block.au-target.phw-content-block-nd > ul > li')))

        # Scrape first page
        job_elements = driver.find_elements(By.CSS_SELECTOR, 'div.content-block.au-target.phw-content-block-nd > ul > li')
        for element in job_elements:
            try:
                title = element.find_element(By.CSS_SELECTOR, 'div > div > span > a > div > span').text
                location = element.find_element(By.CSS_SELECTOR, 'div > div > p > span > span').text
                job_url = element.find_element(By.TAG_NAME, 'a').get_attribute('href')

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

        # Paginate through results
        while True:
            try:
                next_button = driver.find_element(By.CSS_SELECTOR, 'li:nth-child(7) > a > span:nth-child(1) > ppc-content')
                if not next_button.is_displayed():
                    break
                next_button.click()
                time.sleep(3)
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.content-block.au-target.phw-content-block-nd > ul > li')))

                job_elements = driver.find_elements(By.CSS_SELECTOR, 'div.content-block.au-target.phw-content-block-nd > ul > li')
                for element in job_elements:
                    try:
                        title = element.find_element(By.CSS_SELECTOR, 'div > div > span > a > div > span').text
                        location = element.find_element(By.CSS_SELECTOR, 'div > div > p > span > span').text
                        job_url = element.find_element(By.TAG_NAME, 'a').get_attribute('href')

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
            except:
                break

    finally:
        driver.quit()

    return jobs


# For testing this scraper individually
if __name__ == "__main__":
    result = scrape_genentech_jobs()
    print(f"Found {len(result)} internship(s)")
    for job in result:
        print(f"  - {job['title']} at {job['location']}")
