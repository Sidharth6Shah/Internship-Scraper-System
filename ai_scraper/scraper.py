import json
import hashlib
from datetime import datetime, timezone
from anthropic import Anthropic
from ai_scraper.config import ANTHROPIC_API_KEY, KEYWORDS


def scrape_jobs(url, company, source_id):
    client = Anthropic(api_key=ANTHROPIC_API_KEY)

    system_prompt = (
        f"Visit the URL {url} and find all job postings. "
        "Return ONLY a valid JSON array with this exact structure: "
        '[{"title": "Job Title", "company": "Company Name", "url": "https://job-url.com", "location": "Location"}]. '
        "No markdown, no explanation, no additional text. Only the JSON array."
    )

    try:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=4096,
            betas=["server-tool-use-2025-02-24"],
            tools=[
                {
                    "type": "web_fetch_20250910",
                    "name": "web_fetch"
                },
                {
                    "type": "web_search_20250305",
                    "name": "web_search"
                }
            ],
            messages=[
                {
                    "role": "user",
                    "content": system_prompt
                }
            ]
        )

        result_text = ""
        for block in response.content:
            if hasattr(block, 'text'):
                result_text += block.text

        result_text = result_text.strip()
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
