# Internship-Scraper-System
Scraper system that runs automated routine checks for new postings.


Dev. Steps:
1. Duplicate a previous scraper and build it into a unique one.
2. Test locally by running the file. (If it works, make headless true.)
3. To config.py:
    from scrapers.<scrapername> import scrape_<company>_jobs
    Add url, company name and source id to JOB_SOURCES