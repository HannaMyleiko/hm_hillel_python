# each social channel has a type
# and the current number of followers
import time

SocialChannel = tuple[str, int]

# each post has a message and the timestamp when it should be posted
Post = tuple[str, int]


def post_to_youtube(channel, message):
    pass


def post_to_facebook(channel, message):
    pass


def post_to_twitter(channel, message):
    pass


def post_a_message(channel: SocialChannel, message: str) -> None:
    type, _ = channel
    if type == "youtube":
        post_to_youtube(channel, message)
    elif type == "facebook":
        post_to_facebook(channel, message)
    elif type == "twitter":
        post_to_twitter(channel, message)


def process_schedule(posts: list[Post], channels: list[SocialChannel]) -> None:
    for post in posts:
        message, timestamp = post
        for channel in channels:
            if timestamp <= time.time():
                post_a_message(channel, message)