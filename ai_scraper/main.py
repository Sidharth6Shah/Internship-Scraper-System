import time
from db_manager import DBManager
from notifier import Notifier
from ai_scraper.config import AI_JOB_SOURCES
from ai_scraper.scraper import scrape_jobs


def compare_and_update(scraped_jobs, source_id, db_manager, notifier):
    # Get current active jobs from DB
    db_jobs = db_manager.get_active_jobs(source_id)
    db_job_ids = set(db_jobs.keys())
    scraped_job_ids = {job['job_id'] for job in scraped_jobs}

    # Find differences
    new_job_ids = scraped_job_ids - db_job_ids
    existing_job_ids = scraped_job_ids & db_job_ids
    removed_job_ids = db_job_ids - scraped_job_ids

    # Process NEW jobs
    for job in scraped_jobs:
        if job['job_id'] in new_job_ids:
            db_manager.insert_job(job)
            notifier.send_new_job_notification(job)
            print(f"✅ New job: {job['title']}")

    # Process EXISTING jobs (update last_seen)
    for job_id in existing_job_ids:
        db_manager.update_last_seen(job_id)

    # Process REMOVED jobs
    for job_id in removed_job_ids:
        db_manager.mark_as_removed(job_id)
        print(f"❌ Removed: {db_jobs[job_id]['title']}")

    print(f"Summary: {len(new_job_ids)} new, {len(existing_job_ids)} existing, {len(removed_job_ids)} removed")


def lambda_handler(event, context):
    db_manager = DBManager()
    notifier = Notifier()

    for i, source in enumerate(AI_JOB_SOURCES):
        print(f"\n🔍 Scraping {source['company']}...")

        scraped_jobs = scrape_jobs(
            url=source['url'],
            company=source['company'],
            source_id=source['source_id'],
            requires_search=source.get('requires_search', False)
        )

        print(f"Found {len(scraped_jobs)} internships")
        compare_and_update(scraped_jobs, source['source_id'], db_manager, notifier)

        # Wait 60 seconds between companies to avoid rate limiting (except after last company)
        if i < len(AI_JOB_SOURCES) - 1:
            print("⏱️  Waiting 60 seconds to avoid rate limits...")
            time.sleep(60)

    return {"statusCode": 200, "body": "AI Scraping complete"}


if __name__ == "__main__":
    lambda_handler(None, None)
