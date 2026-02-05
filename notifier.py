# Notification module
import requests
import time
from config import DISCORD_WEBHOOK_URL


class Notifier:
    def __init__(self):
        self.webhook_url = DISCORD_WEBHOOK_URL

    def send_new_job_notification(self, job):
        message = (
            f"🆕 **New Internship!**\n"
            f"**{job['title']}** at **{job['company']}**\n"
            f"📍 {job['location']}\n"
            f"🔗 {job['url']}"
        )

        try:
            response = requests.post(self.webhook_url, json={"content": message})
            response.raise_for_status()
            # Add delay to avoid Discord rate limiting (max 5 requests per 2 seconds)
            time.sleep(0.5)
        except requests.exceptions.RequestException as e:
            print(f"Failed to send Discord notification: {e}")

    def send_test_notification(self, message):
        try:
            response = requests.post(self.webhook_url, json={"content": message})
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Failed to send test notification: {e}")
