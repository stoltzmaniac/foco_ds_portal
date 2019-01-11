import re

from textblob import TextBlob

import pandas as pd
import altair as alt


def download_csv() -> pd.DataFrame:
    url = "http://samplecsvs.s3.amazonaws.com/SacramentocrimeJanuary2006.csv"
    data = pd.read_csv(url)
    return data[0:1000]


def plot_altair() -> alt.Chart:
    data = download_csv()
    base = alt.Chart(data)
    # Build chart
    bar = base.mark_bar().encode(x=alt.X("latitude", bin=True, axis=None), y="count()")
    return bar


def clean_tweet(raw_tweet_text: str):
    """ Utility function to clean tweet text by removing links, special characters using simple regex statements."""
    return " ".join(
        re.sub(
            "(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])| (\w+:\ /  \ /  \S+)",
            " ",
            raw_tweet_text,
        ).split()
    )


def analyze_tweet_sentiment(tweet_list: list) -> list:
    tweet_sentiment = []
    positive = neutral = negative = 0
    for tweet in tweet_list:
        twt = {}
        analysis = TextBlob(clean_tweet(tweet["text"]))
        if analysis.sentiment.polarity > 0:
            twt["positive"] = tweet["text"]
            positive += 1
        elif analysis.sentiment.polarity == 0:
            twt["neutral"] = tweet["text"]
            neutral += 1
        else:
            twt["negative"] = tweet["text"]
            negative += 1
        tweet_sentiment.append(twt)
    total_sentiment = {"positive": positive, "neutral": neutral, "negative": negative}
    return [tweet_sentiment, total_sentiment]
