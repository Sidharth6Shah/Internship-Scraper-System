import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
DYNAMODB_TABLE_NAME = os.getenv("DYNAMODB_TABLE_NAME")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

AI_JOB_SOURCES = [
    {
        "url": "https://neuralink.com/careers/",
        "company": "Neuralink",
        "source_id": "neuralink_ai"
    },
    {
        "url": "https://jobs.ashbyhq.com/cohere",
        "company": "Cohere",
        "source_id": "cohere_ai"
    },
    {
        "url": "https://careers.gene.com/us/en",
        "company": "Genentech",
        "source_id": "genentech_ai",
        "requires_search": True
    },
    {
        "url": "https://www.anthropic.com/careers/jobs",
        "company": "Anthropic",
        "source_id": "anthropic_ai"
    },
    {
        "url": "https://openai.com/careers/search/",
        "company": "OpenAI",
        "source_id": "openai_ai"
    },
    {
        "url": "https://job-boards.greenhouse.io/deepmind",
        "company": "DeepMind",
        "source_id": "deepmind_ai"
    }
]

KEYWORDS = ["intern", "co-op", "co op", "coop", "student"]
