import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
DYNAMODB_TABLE_NAME = os.getenv("DYNAMODB_TABLE_NAME")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

AI_JOB_SOURCES = [
    {
        "url": "https://neuralink.com/careers/",
        "company": "Neuralink",
        "source_id": "neuralink_ai"
    },
    {
        "url": "https://cohere.com/careers",
        "company": "Cohere",
        "source_id": "cohere_ai"
    },
    {
        "url": "https://www.gene.com/careers",
        "company": "Genentech",
        "source_id": "genentech_ai"
    },
    {
        "url": "https://www.anthropic.com/careers",
        "company": "Anthropic",
        "source_id": "anthropic_ai"
    },
    {
        "url": "https://openai.com/careers/",
        "company": "OpenAI",
        "source_id": "openai_ai"
    },
    {
        "url": "https://www.deepmind.com/careers",
        "company": "DeepMind",
        "source_id": "deepmind_ai"
    },
    {
        "url": "https://scale.com/careers",
        "company": "Scale AI",
        "source_id": "scale_ai"
    }
]

KEYWORDS = ["intern", "co-op", "co op", "student"]
