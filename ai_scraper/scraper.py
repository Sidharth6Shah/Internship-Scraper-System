import json
import hashlib
import time
import os
from datetime import datetime, timezone
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from openai import OpenAI
from ai_scraper.config import OPENAI_API_KEY, KEYWORDS


def scrape_jobs(url, company, source_id, requires_search=False):
    client = OpenAI(api_key=OPENAI_API_KEY)
    driver = None

    try:
        # Chrome options
        chrome_options = Options()
        chrome_options.add_argument('--headless=new')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')

        # Check if running in Lambda (use Lambda paths) or locally
        if os.path.exists('/opt/chrome/chrome-linux64/chrome'):
            chrome_options.add_argument('--single-process')
            chrome_options.add_argument('--disable-dev-tools')
            chrome_options.add_argument('--no-zygote')
            chrome_options.binary_location = '/opt/chrome/chrome-linux64/chrome'
            driver = webdriver.Chrome(
                options=chrome_options,
                service=webdriver.ChromeService(executable_path='/opt/chromedriver')
            )
        else:
            # Local execution - use system Chrome (don't use single-process on Mac)
            driver = webdriver.Chrome(options=chrome_options)

        # Load the page with Selenium (renders JavaScript)
        driver.get(url)
        time.sleep(5)  # Wait for JavaScript to load

        # If search is required, interact with search input
        if requires_search:
            try:
                # First, try to dismiss any cookie/GDPR overlays
                overlay_dismiss_selectors = [
                    '#onetrust-accept-btn-handler',  # OneTrust
                    'button[id*="accept"]',
                    'button[id*="cookie"]',
                    'button[class*="accept"]',
                    'button[class*="cookie"]'
                ]

                for selector in overlay_dismiss_selectors:
                    try:
                        buttons = driver.find_elements(By.CSS_SELECTOR, selector)
                        if buttons:
                            buttons[0].click()
                            time.sleep(1)
                            print(f"  Dismissed overlay on {company} page")
                            break
                    except:
                        continue

                # Try common search input selectors
                search_input = None
                selectors = [
                    'input[type="text"]',
                    'input[type="search"]',
                    'input[placeholder*="search" i]',
                    'input[placeholder*="keyword" i]',
                    'input[aria-label*="search" i]',
                    'input'
                ]

                for selector in selectors:
                    try:
                        inputs = driver.find_elements(By.CSS_SELECTOR, selector)
                        if inputs:
                            search_input = inputs[0]
                            break
                    except:
                        continue

                if search_input:
                    search_input.click()
                    search_input.send_keys('intern')
                    search_input.send_keys(Keys.RETURN)
                    time.sleep(5)  # Wait for search results to load
                    print(f"  Searched for 'intern' on {company} page")
                else:
                    print(f"  Warning: Could not find search input on {company} page")
            except Exception as e:
                print(f"  Warning: Search interaction failed for {company}: {str(e)}")

        # Get the rendered HTML
        page_content = driver.page_source[:100000]  # Limit to first 100k chars

        # Close driver before making API call
        driver.quit()
        driver = None

        # Ask GPT to extract jobs
        system_prompt = (
            "You are analyzing a careers page. Extract all job postings and return ONLY a valid JSON array "
            "with this exact structure: "
            '[{"title": "Job Title", "company": "Company Name", "url": "https://job-url.com", "location": "Location"}]. '
            "For the URL field, if you find relative URLs, convert them to absolute URLs using the domain from the page. "
            "No markdown, no explanation, no additional text. Only the JSON array."
        )

        user_prompt = f"Here is the HTML content from {url}:\n\n{page_content}\n\nExtract all job postings."

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0,
            max_tokens=16384  # Increased to handle large job lists
        )

        result_text = response.choices[0].message.content.strip()

        # Clean markdown formatting if present
        if result_text.startswith("```json"):
            result_text = result_text[7:]
        if result_text.startswith("```"):
            result_text = result_text[3:]
        if result_text.endswith("```"):
            result_text = result_text[:-3]
        result_text = result_text.strip()

        jobs = json.loads(result_text)

        filtered_jobs = []
        for job in jobs:
            title_lower = job.get('title', '').lower()
            if any(keyword.lower() in title_lower for keyword in KEYWORDS):
                job_url = job.get('url', '')
                job_id = hashlib.md5(job_url.encode()).hexdigest()
                now = datetime.now(timezone.utc).isoformat()

                job['job_id'] = job_id
                job['source'] = source_id
                job['status'] = 'active'
                job['first_seen'] = now
                job['last_seen'] = now

                filtered_jobs.append(job)

        return filtered_jobs

    except Exception as e:
        print(f"Error scraping {company}: {str(e)}")
        return []

    finally:
        if driver is not None:
            try:
                driver.quit()
            except:
                pass
