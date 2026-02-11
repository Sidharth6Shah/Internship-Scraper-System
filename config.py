# Settings file
import os
from dotenv import load_dotenv

load_dotenv()
from scrapers.neuralink import scrape_neuralink_jobs
from scrapers.astrazeneca import scrape_astrazeneca_jobs
from scrapers.cohere import scrape_cohere_jobs
from scrapers.genentech import scrape_genentech_jobs

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
DYNAMODB_TABLE_NAME = os.getenv("DYNAMODB_TABLE_NAME")

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
    {
        "scraper_function": scrape_cohere_jobs,
        "company": "Cohere",
        "source_id": "cohere"
    },
    {
        "scraper_function": scrape_genentech_jobs,
        "company": "Genentech",
        "source_id": "genentech"
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
