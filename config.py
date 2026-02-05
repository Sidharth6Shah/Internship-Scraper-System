# ============================================
# CONFIGURATION
# ============================================
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import scraper functions
from scrapers.neuralink import scrape_neuralink_jobs
from scrapers.astrazeneca import scrape_astrazeneca_jobs

# Discord webhook URL for notifications
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

# DynamoDB table name
DYNAMODB_TABLE_NAME = os.getenv("DYNAMODB_TABLE_NAME")

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
