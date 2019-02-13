# project/server/GregHilston/views.py


from flask import render_template, Blueprint, url_for, redirect, flash, request, jsonify
from flask_login import login_required

from project.server.stoltzmaniac.utils import download_csv, plot_altair
from project.server.twitter.mongo_forms import TwitterForm
from project.server.twitter.utils import twitter_search
from project.server.stoltzmaniac.utils import analyze_tweet_sentiment


GregHilston_blueprint = Blueprint(
    "GregHilston", __name__, url_prefix="/GregHilston"
)


@GregHilston_blueprint.route("/", methods=["GET"])
def home():
    return render_template("GregHilston/home.html")
