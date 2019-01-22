import re
import base64
import requests as requests_lib
from io import BytesIO
import datetime

from textblob import TextBlob
import numpy as np
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
from PIL import Image
from wordcloud import WordCloud, STOPWORDS
# from sklearn.ensemble import RandomForestRegressor
# from sklearn.model_selection import train_test_split


def download_csv() -> pd.DataFrame:
    url = "http://samplecsvs.s3.amazonaws.com/SacramentocrimeJanuary2006.csv"
    data = pd.read_csv(url)
    return data


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


def clean_list_of_text(wordcloud_data):
    raw_string = ''.join(wordcloud_data)
    no_links = re.sub(r'http\S+', '', raw_string)
    no_unicode = re.sub(r"\\[a-z][a-z]?[0-9]+", '', no_links)
    no_special_characters = re.sub('[^A-Za-z ]+', '', no_unicode)
    words = no_special_characters.split(" ")
    words = [w for w in words if len(w) > 2]  # ignore a, an, be, ...
    words = [w.lower() for w in words]
    words = [w for w in words if w not in STOPWORDS]
    return words


def generate_wordcloud(wordcloud_data, image_url) -> plt:
    words = clean_list_of_text(wordcloud_data)
    img_response = requests_lib.get(image_url)
    img = Image.open(BytesIO(img_response.content))
    mask = np.array(img)
    wc = WordCloud(background_color="white", max_words=2000, mask=mask)
    clean_string = ','.join(words)
    wc.generate(clean_string)
    f = plt.figure(figsize=(15, 15))
    f.add_subplot(1, 2, 1)
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    tmpfile = BytesIO()
    plt.savefig(tmpfile, format='png', bbox_inches="tight", pad_inches=0)
    encoded = base64.b64encode(tmpfile.getvalue())
    return encoded


# def logistic_regression():
#     data = download_csv()
#     data = data.dropna()
#     data['timestamp'] = data['cdatetime'].apply(lambda x: datetime.datetime.strptime(x, "%m/%d/%y %H:%M"))
#     data['date'] = data['timestamp'].dt.date
#     data['hour'] = data['timestamp'].dt.hour
#     data['day_of_week'] = data['timestamp'].dt.weekday
#     d = data.set_index('timestamp')
#     d = d[['district']]
#     d['tod'] = d.index.hour
#     d['dow'] = d.index.weekday
#     add_tod = pd.get_dummies(d['tod'], prefix='tod', drop_first=True)
#     d = d.join(add_tod)
#     add_dow = pd.get_dummies(d['dow'], prefix='dow', drop_first=True)
#     d = d.join(add_dow)
#     labels = np.array(d['district'])
#     features = d.reset_index().drop(['timestamp', 'district', 'tod', 'dow'], axis=1)
#     feature_list = list(features.columns)
#     features = np.array(features)
#     train_features, test_features, train_labels, test_labels = train_test_split(features,
#                                                                                 labels,
#                                                                                 test_size=0.25,
#                                                                                 random_state=42)
#     rf = RandomForestRegressor(n_estimators=1000, random_state=42)




