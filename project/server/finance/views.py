# project/server/stoltzmaniac/views.py
from flask import render_template, Blueprint, url_for, redirect, flash, request, jsonify
from flask_login import login_required
import pandas as pd

from project.server.stoltzmaniac.utils import download_csv, plot_altair
from project.server.twitter.mongo_forms import TwitterForm, TwitterTimelineForm
from project.server.twitter.utils import twitter_search, twitter_timeline, twitter_congressional_list, lookup_recent_tweets, store_daily_public_tweets
from project.server.stoltzmaniac.utils import analyze_tweet_sentiment, generate_wordcloud
from project.server.finance.forms import TickerForm
from project.server.finance.utils import quandl, plot_line


finance_blueprint = Blueprint("finance", __name__, url_prefix="/finance")


@finance_blueprint.route("/", methods=["GET"])
def home():
    form = TickerForm()
    return render_template("finance/home.html", myform=form)


@finance_blueprint.route("/data/<symbols>/<start_date>/<end_date>", methods=["POST"])
def get_daily_adj_close(symbols, start_date, end_date):
    """symbols should be comma separated with no spaces"""
    tickers = symbols.split(',')
    data = quandl.get_table('WIKI/PRICES', ticker=tickers,
                            qopts={'columns': ['ticker', 'date', 'adj_close']},
                            date={'gte': start_date, 'lte': end_date},
                            paginate=True)
    data = data.reset_index()
    plot = plot_line(data)
    return plot.to_html()


