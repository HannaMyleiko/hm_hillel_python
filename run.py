import time
import logging
import social_channels
from social import Post, process_schedule

def main():
    posts = []
    for i in range(10):
        if i % 3 != 0:
            posts.append(Post(f"Message-{i}", time.time()))
        else:
            posts.append(Post(f"Message-{i}", time.time() + i ))
    channels = [
        social_channels.get_channel("youtube"),
        social_channels.get_channel("twitter"),
    ]
    process_schedule(posts, channels)


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

main()


