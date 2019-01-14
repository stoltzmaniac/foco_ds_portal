# project/server/stoltzmaniac/views.py
from flask import render_template, Blueprint, url_for, redirect, flash, request, jsonify
from flask_login import login_required
import pandas as pd

from project.server.stoltzmaniac.utils import download_csv, plot_altair
from project.server.twitter.mongo_forms import TwitterForm, TwitterTimelineForm
from project.server.twitter.utils import twitter_search, twitter_timeline, twitter_congressional_list, twitter_timeline2
from project.server.stoltzmaniac.utils import analyze_tweet_sentiment, generate_wordcloud


stoltzmaniac_blueprint = Blueprint("stoltzmaniac", __name__, url_prefix="/stoltzmaniac")


@stoltzmaniac_blueprint.route("/", methods=["GET"])
def home():
    return render_template("stoltzmaniac/home.html")


@stoltzmaniac_blueprint.route("/csv_example", methods=["GET"])
def csv_example():
    data = download_csv()
    return data.to_html()


@stoltzmaniac_blueprint.route("/altair_example", methods=["GET"])
def altair_example():
    plot = plot_altair()
    return render_template("stoltzmaniac/altair_plot.html", plot=plot.to_html())


@stoltzmaniac_blueprint.route("/twitter_sentiment", methods=["GET", "POST"])
@login_required
def twitter_sentiment():
    form = TwitterForm(request.form)
    if request.method == "GET":
        return render_template("stoltzmaniac/twitter_sentiment.html", myform=form)

    elif request.method == "POST" and form.validate_on_submit():
        chart_data = []
        data = twitter_search(request)
        sentiment = analyze_tweet_sentiment(data)
        return render_template(
            "stoltzmaniac/twitter_sentiment.html",
            myform=form,
            chart_data=sentiment[1],
            tweets=sentiment[0],
        )


# TODO: Clean up how to pass request only once
@stoltzmaniac_blueprint.route("/twitter_timeline", methods=["GET", "POST"])
@login_required
def tweet_timeline():
    form = TwitterTimelineForm(request.form)
    if request.method == "GET":
        return render_template("stoltzmaniac/twitter_timeline.html", myform=form)

    elif request.method == "POST" and form.validate_on_submit():
        wordcloud_data = twitter_timeline(request)
        form_data = request.form
        wordcloud = generate_wordcloud(wordcloud_data, form_data['image_url'])
        return render_template(
            "stoltzmaniac/twitter_timeline.html",
            myform=form,
            wordcloud=wordcloud.decode('utf-8'),
        )


@stoltzmaniac_blueprint.route('/congress', methods=['GET'])
def congressional_tweets():
    data = twitter_congressional_list()
    df = pd.DataFrame(data)
    s_rep = df[(df['party'] == 'republican') & (df['chamber'] == 'senate')].to_dict(orient='records')
    s_dem = df[(df['party'] == 'democrat') & (df['chamber'] == 'senate')].to_dict(orient='records')
    h_rep = df[(df['party'] == 'republican') & (df['chamber'] == 'house_of_representatives')].to_dict(orient='records')
    h_dem = df[(df['party'] == 'democrat') & (df['chamber'] == 'house_of_representatives')].to_dict(orient='records')
    return render_template('stoltzmaniac/congress.html', s_rep=s_rep, s_dem=s_dem, h_dem=h_dem, h_rep=h_rep, wordcloud='')


@stoltzmaniac_blueprint.route("/generate_cloud/<screen_name>/<party>", methods=["POST"])
def generate_wc(screen_name, party):
    img_url = 'https://i.postimg.cc/VkPvgL8K/ele.png'
    if party == 'democrat':
        img_url = 'https://i.postimg.cc/GmvWPbLJ/donk.jpg'
    wordcloud_data = twitter_timeline2(screen_name)
    wordcloud = generate_wordcloud(wordcloud_data, img_url)
    return wordcloud.decode('utf-8')


# @stoltzmaniac_blueprint.route("/generate_cloud/<screen_name>/<img_url>", methods=["POST"])
# def generate_wc(screen_name, img_url):
#     wordcloud_data = twitter_timeline2(screen_name)
#     wordcloud = generate_wordcloud(wordcloud_data, img_url)
#     return jsonify(wordcloud=wordcloud.decode('utf-8'))
