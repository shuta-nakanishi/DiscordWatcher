import os

from dotenv import load_dotenv

load_dotenv()


class Config:

    DISCORD_TOKEN = os.getenv(
        "DISCORD_TOKEN"
    )

    TARGET_USER_ID = int(
        os.getenv("TARGET_USER_ID")
    )

    NOTIFY_CHANNEL_ID = int(
        os.getenv("NOTIFY_CHANNEL_ID")
    )

    STATUS_STORAGE = os.getenv(
        "STATUS_STORAGE",
        "file"
    )

    S3_BUCKET_NAME = os.getenv(
        "S3_BUCKET_NAME"
    )

    S3_STATUS_KEY = os.getenv(
        "S3_STATUS_KEY",
        "status.json"
    )