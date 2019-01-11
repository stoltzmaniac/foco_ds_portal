# project/server/new_user_addition_example/views.py


from flask import render_template, Blueprint, url_for, redirect, flash, request, jsonify
from flask_login import login_required

from project.server.stoltzmaniac.utils import download_csv, plot_altair
from project.server.twitter.mongo_forms import TwitterForm
from project.server.twitter.utils import twitter_search
from project.server.stoltzmaniac.utils import analyze_tweet_sentiment


new_user_addition_example_blueprint = Blueprint(
    "new_user_addition_example", __name__, url_prefix="/new_user_addition_example"
)


@new_user_addition_example_blueprint.route("/", methods=["GET"])
def home():
    return render_template("new_user_addition_example/home.html")
