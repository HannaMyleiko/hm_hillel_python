import abc
import logging

class SocialChannel(abc.ABC):

    channel_name: str
    @abc.abstractmethod
    def post(self, message: str):
        """"""

    def get_name(self):
        return self.channel_name

class YoutubeChannel(SocialChannel):
    channel_name = "YouTube"
    def post(self, message: str):
        logging.info(f"Posted to Youtube: {message}")
class FacebookChannel(SocialChannel):
    channel_name = "Facebook"
    def post(self, message: str):
        logging.info(f"Posted to Facebook: {message}")
class TwitterChannel(SocialChannel):
    channel_name = "Twitter"
    def post(self, message: str):
        logging.info(f"Posted to Twitter: {message}")



CHANNEL_LIST={
    "youtube": YoutubeChannel(),
    "facebook": FacebookChannel(),
    "twitter": TwitterChannel()
}

def get_channel(channel_name: str)->SocialChannel:
    return CHANNEL_LIST.get(channel_name.lower())