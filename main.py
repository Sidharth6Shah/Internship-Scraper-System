"""
Main Orchestrator - Coordinates scraping, database updates, and notifications
"""
from db_manager import DBManager
from notifier import Notifier
from config import JOB_SOURCES
from scrapers.scraper import scrape_jobs


def compare_and_update(scraped_jobs, source_id, db_manager, notifier):
    """
    Compare scraped jobs with database and update accordingly

    Args:
        scraped_jobs (list): List of job dictionaries from scraper
        source_id (str): Source identifier
        db_manager (DBManager): Database manager instance
        notifier (Notifier): Notifier instance
    """
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
    """
    Main function - will be called by AWS Lambda

    Args:
        event: Lambda event object
        context: Lambda context object

    Returns:
        dict: Response with statusCode and body
    """
    # Initialize managers
    db_manager = DBManager()
    notifier = Notifier()

    # Process each job source
    for source in JOB_SOURCES:
        print(f"\n🔍 Scraping {source['company']}...")

        # Scrape jobs
        scraped_jobs = scrape_jobs(source['url'], source['company'], source['source_id'])
        print(f"Found {len(scraped_jobs)} internships")

        # Compare and update
        compare_and_update(scraped_jobs, source['source_id'], db_manager, notifier)

    return {"statusCode": 200, "body": "Scraping complete"}


# For local testing
if __name__ == "__main__":
    lambda_handler(None, None)
