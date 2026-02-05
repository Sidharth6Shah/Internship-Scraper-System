# ============================================
# CONFIGURATION
# ============================================

# Import scraper functions
from scrapers.neuralink import scrape_neuralink_jobs
from scrapers.astrazeneca import scrape_astrazeneca_jobs

# Discord webhook URL for notifications
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1467274396728299663/_558Bm4j7KWBDq0qJmW_meDbIT8bWJNEL0XLQS12WYXBOPnpZMz7rDuLc1QodiNxvn4b"

# DynamoDB table name
DYNAMODB_TABLE_NAME = "InternshipDB"

# Job sources to scrape
# Each source needs:
# - scraper_function: the function to call for scraping
# - company: company name for display
# - source_id: unique identifier for this source
JOB_SOURCES = [
    {
        "scraper_function": scrape_neuralink_jobs,
        "company": "Neuralink",
        "source_id": "neuralink"
    },
    # {
    #     "scraper_function": scrape_astrazeneca_jobs,
    #     "company": "AstraZeneca",
    #     "source_id": "astrazeneca"
    # },
    
    # Add more scrapers here as you build them
    # {
    #     "scraper_function": scrape_anthropic_jobs,
    #     "company": "Anthropic",
    #     "source_id": "anthropic"
    # },
]
