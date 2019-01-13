# project/server/stoltzmaniac/views.py


from flask import render_template, Blueprint, url_for, redirect, flash, request, jsonify
from flask_login import login_required

from project.server.stoltzmaniac.utils import download_csv, plot_altair
from project.server.twitter.mongo_forms import TwitterForm, TwitterTimelineForm
from project.server.twitter.utils import twitter_search, twitter_timeline
from project.server.stoltzmaniac.utils import analyze_tweet_sentiment, generate_wordcloud, get_congressional_list


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
    data = get_congressional_list()
    house = data.house
    senate = data.senate
    print(house)
    print(senate)
    return jsonify({'hi': 'there'})
