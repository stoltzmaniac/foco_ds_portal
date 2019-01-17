import os
import json
import tweepy
from pymongo import MongoClient


TWTR_CONSUMER_KEY = os.getenv("TWTR_CONSUMER_KEY")
TWTR_CONSUMER_SECRET = os.getenv("TWTR_CONSUMER_SECRET")
TWTR_TOKEN_KEY = os.getenv("TWTR_TOKEN_KEY")
TWTR_TOKEN_SECRET = os.getenv("TWTR_TOKEN_SECRET")
MONGO_URI = os.getenv("MONGO_URI")


client = MongoClient(MONGO_URI)
db = client.get_database()
twitter_collection = db.tweets


auth = tweepy.OAuthHandler(TWTR_CONSUMER_KEY, TWTR_CONSUMER_SECRET)
auth.set_access_token(TWTR_TOKEN_KEY, TWTR_TOKEN_SECRET)
api = tweepy.API(auth)


class TweetListener(tweepy.StreamListener):

    def on_status(self, status):
        pass

    def on_data(self, data):
        all_data = json.loads(data)
        print(all_data)
        twitter_collection.insert_one(all_data)

    def on_error(self, status_code):
        if status_code == 420:
            return False


stream = tweepy.Stream(auth=api.auth, listener=TweetListener())
stream.filter(track=["rstats"])
