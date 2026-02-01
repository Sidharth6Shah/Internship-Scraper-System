# ============================================
# CONFIGURATION
# ============================================

# Discord webhook URL for notifications
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1467274396728299663/_558Bm4j7KWBDq0qJmW_meDbIT8bWJNEL0XLQS12WYXBOPnpZMz7rDuLc1QodiNxvn4b"

# DynamoDB table name
DYNAMODB_TABLE_NAME = "InternshipDB"

# Job sources to scrape
JOB_SOURCES = [
    {
        "url": "https://jobs.lever.co/anthropic",
        "company": "Anthropic",
        "source_id": "lever_anthropic"
    },
    # Add more sources here as needed
    # {
    #     "url": "https://example.com/careers",
    #     "company": "Example Corp",
    #     "source_id": "example_corp"
    # },
]
