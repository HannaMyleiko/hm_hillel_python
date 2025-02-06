from datetime import datetime
import time
import logging
from dataclasses import dataclass

from social_channels import SocialChannel

@dataclass
class Post:
    message: str
    timestamp: float


def post_a_message(channel: SocialChannel, message: str) -> None:
    channel.post(message)

def process_schedule(posts: list[Post], channels: list[SocialChannel]) -> None:
    for post in posts:
        for channel in channels:
            if post.timestamp <= time.time():
                post_a_message(channel, post.message)
            else:
                logging.info(f"It's not time for the following post yet ({datetime.fromtimestamp(post.timestamp)}), so it has not been sent to {channel.get_name()}: {post.message}")