"""Full test of AI scraper (no database, with delays)"""
import time
from ai_scraper.scraper import scrape_jobs
from ai_scraper.config import AI_JOB_SOURCES

print("Testing AI scraper (all companies)...\n")
print("=" * 80)

total = 0
for i, source in enumerate(AI_JOB_SOURCES, 1):
    print(f"\n[{i}/{len(AI_JOB_SOURCES)}] 🔍 {source['company']}...")
    print(f"URL: {source['url']}")

    jobs = scrape_jobs(
        url=source['url'],
        company=source['company'],
        source_id=source['source_id'],
        requires_search=source.get('requires_search', False)
    )

    print(f"✅ Found {len(jobs)} positions")
    if jobs:
        for job in jobs[:3]:
            print(f"  - {job['title']}")
        if len(jobs) > 3:
            print(f"  ... and {len(jobs) - 3} more")

    total += len(jobs)
    print("-" * 80)

    # Wait 60 seconds between companies to avoid rate limiting
    if i < len(AI_JOB_SOURCES):
        print("⏱️  Waiting 60 seconds to avoid rate limits...")
        time.sleep(60)

print(f"\n🎉 TOTAL: Found {total} internship/student positions across {len(AI_JOB_SOURCES)} companies")
