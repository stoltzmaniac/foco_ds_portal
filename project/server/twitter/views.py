# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
import time
import datetime
from urllib.parse import quote_plus

import pandas as pd
from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
    jsonify,
    session,
)
from flask_login import login_required

from project.server import mdb

from project.server.utils import flash_errors, twtr
from project.server.twitter.mongo_forms import TwitterForm
from project.server.twitter.utils import twitter_search, twitter_timeline


twitter_blueprint = Blueprint("twitter", __name__, url_prefix="/twitter")


@twitter_blueprint.route("/", methods=["GET", "POST"])
@login_required
def twitter():
    """Adding Twitter data to Mongo database via form"""
    user_id = str(session["user_id"])
    form = TwitterForm(request.form)
    tweets = mdb.db.tweets
    data = tweets.find({"one_hundred_id": user_id})
    output = [i for i in data]

    if request.method == "GET":
        return render_template("twitter/index.html", myform=form, output=output)

    elif request.method == "POST" and form.validate_on_submit():
        data = twitter_search(request)
        for d in data:
            d["one_hundred_id"] = user_id
            tweets.insert_one(d)
        return redirect(url_for("twitter.twitter"))

    else:
        return jsonify({"something": "went wrong"})
