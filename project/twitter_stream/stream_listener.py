import os
import tweepy


MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGODB_DB")
MONGO_HOST = os.getenv("MONGODB_HOST")
MONGO_PORT = os.getenv("MONGODB_PORT")
TWTR_CONSUMER_KEY = os.getenv("TWTR_CONSUMER_KEY")
TWTR_CONSUMER_SECRET = os.getenv("TWTR_CONSUMER_SECRET")
TWTR_TOKEN_KEY = os.getenv("TWTR_TOKEN_KEY")
TWTR_TOKEN_SECRET = os.getenv("TWTR_TOKEN_SECRET")


auth = tweepy.OAuthHandler(TWTR_CONSUMER_KEY, TWTR_CONSUMER_SECRET)
auth.set_access_token(TWTR_TOKEN_KEY, TWTR_TOKEN_SECRET)
api = tweepy.API(auth)


class TweetListener(tweepy.StreamListener):

    def on_status(self, status):
        print(status.text)

    def on_error(self, status_code):
        if status_code == 420:
            return False


stream = tweepy.Stream(auth=api.auth, listener=TweetListener())
stream.filter(track=["rstats"])
