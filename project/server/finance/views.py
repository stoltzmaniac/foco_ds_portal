# project/server/stoltzmaniac/views.py
from flask import render_template, Blueprint, url_for, redirect, flash, request, jsonify
from flask_login import login_required
import pandas as pd

from project.server.stoltzmaniac.utils import download_csv, plot_altair
from project.server.twitter.mongo_forms import TwitterForm, TwitterTimelineForm
from project.server.twitter.utils import twitter_search, twitter_timeline, twitter_congressional_list, lookup_recent_tweets, store_daily_public_tweets
from project.server.stoltzmaniac.utils import analyze_tweet_sentiment, generate_wordcloud
from project.server.finance.forms import TickerForm
from project.server.finance.utils import QuandlData, FinancePlots


finance_blueprint = Blueprint("finance", __name__, url_prefix="/finance")


@finance_blueprint.route("/", methods=["GET"])
def home():
    form = TickerForm()
    return render_template("finance/home.html", myform=form)


@finance_blueprint.route("/data/<tickers>/<start_date>/<end_date>", methods=["POST"])
def plot_tickers_over_time(tickers, start_date, end_date):
    """symbols should be comma separated with no spaces"""
    symbols = tickers.split(',')
    qd = QuandlData()
    fp = FinancePlots()
    data = qd.daily_close_ticker_request(symbols, start_date, end_date)
    plot = fp.line_plot(data, x_axis='date', y_axis='adj_close', color='ticker')
    return plot


