# project/server/stoltzmaniac/views.py
from flask import (
    render_template,
    Blueprint,
    url_for,
    redirect,
    flash,
    request,
    jsonify,
    session,
)
from flask_login import login_required
import pandas as pd
import numpy as np
from urllib.parse import unquote
import statsmodels.api as sm
import plotly.graph_objs as go
import plotly.plotly as py

from project.server.utils import S3
from project.server.utilities.plotting import BasicPlot
from project.server.stoltzmaniac.utils import download_csv, plot_altair
from project.server.stoltzmaniac.forms import FileUploadForm
from project.server.twitter.mongo_forms import TwitterForm, TwitterTimelineForm
from project.server.twitter.utils import (
    twitter_search,
    twitter_timeline,
    twitter_congressional_list,
    lookup_recent_tweets,
    store_daily_public_tweets,
)
from project.server.stoltzmaniac.utils import (
    analyze_tweet_sentiment,
    generate_wordcloud,
)


stoltzmaniac_blueprint = Blueprint("stoltzmaniac", __name__, url_prefix="/stoltzmaniac")


@stoltzmaniac_blueprint.route("/", methods=["GET"])
def home():
    return render_template("stoltzmaniac/home.html")


@stoltzmaniac_blueprint.route("/drop_files", methods=["GET"])
def drop_files():
    return render_template("stoltzmaniac/drop_files.html")


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
        form_data = form.data
        data = twitter_search(
            search_term=form_data["search_term"], count=form_data["count"]
        )
        sentiment = analyze_tweet_sentiment(data)
        return render_template(
            "stoltzmaniac/twitter_sentiment.html",
            myform=form,
            chart_data=sentiment[1],
            tweets=sentiment[0],
        )


@stoltzmaniac_blueprint.route("/twitter_timeline", methods=["GET", "POST"])
@login_required
def tweet_timeline():
    form = TwitterTimelineForm(request.form)
    if request.method == "GET":
        return render_template("stoltzmaniac/twitter_timeline.html", myform=form)

    elif request.method == "POST" and form.validate_on_submit():
        form_data = form.data
        wordcloud_data = twitter_timeline(form_data["username"])
        wordcloud = generate_wordcloud(wordcloud_data, form_data["image_url"])
        return render_template(
            "stoltzmaniac/twitter_timeline.html",
            myform=form,
            wordcloud=wordcloud.decode("utf-8"),
        )


@stoltzmaniac_blueprint.route("/congress", methods=["GET"])
@login_required
def congressional_tweets():
    foco_ds_purpose = "congressional_tweets"
    data = lookup_recent_tweets(foco_ds_purpose)
    if not data:
        data = twitter_congressional_list()
        w_data = store_daily_public_tweets(data, foco_ds_purpose)
    df = pd.DataFrame(data)
    s_rep = df[(df["party"] == "republican") & (df["chamber"] == "senate")].to_dict(
        orient="records"
    )
    s_dem = df[(df["party"] == "democrat") & (df["chamber"] == "senate")].to_dict(
        orient="records"
    )
    h_rep = df[
        (df["party"] == "republican") & (df["chamber"] == "house_of_representatives")
    ].to_dict(orient="records")
    h_dem = df[
        (df["party"] == "democrat") & (df["chamber"] == "house_of_representatives")
    ].to_dict(orient="records")
    return render_template(
        "stoltzmaniac/congress.html",
        s_rep=s_rep,
        s_dem=s_dem,
        h_dem=h_dem,
        h_rep=h_rep,
        wordcloud="",
    )


# TODO: Add CSRF protection
@stoltzmaniac_blueprint.route("/upload_s3", methods=["POST"])
@login_required
def upload_s3():
    for key, f in request.files.items():
        s3 = S3()
        if key.startswith("file"):
            upload, filename = s3.upload_file_by_object(f)
    print(filename)
    return jsonify({"file_location": filename})


# TODO: Add CSRF protection
@stoltzmaniac_blueprint.route("/generate_cloud/<screen_name>/<party>", methods=["POST"])
@login_required
def generate_wc(screen_name, party):
    img_url = "https://i.postimg.cc/VkPvgL8K/ele.png"
    if party == "democrat":
        img_url = "https://i.postimg.cc/GmvWPbLJ/donk.jpg"
    wordcloud_data = twitter_timeline(screen_name)
    wordcloud = generate_wordcloud(wordcloud_data, img_url)
    return wordcloud.decode("utf-8")


@stoltzmaniac_blueprint.route("/data_model", methods=["GET", "POST"])
def data_model():
    form = FileUploadForm()

    if request.method == "GET":
        return render_template(
            "stoltzmaniac/data_model.html", myform=form, data_columns=[], filename=""
        )

    elif request.method == "POST" and form.validate_on_submit():
        form_data = form.data
        filename = ""
        for key, f in form_data.items():
            s3 = S3()
            if key.startswith("file"):
                upload, filename = s3.upload_file_by_object(f)
        data = pd.read_csv(filename)
        data = data.loc[:, data.dtypes == np.float64]
        columns = data.columns.tolist()
        df_head = data.head(10)

        return render_template(
            "stoltzmaniac/data_model.html",
            myform=form,
            data_columns=columns,
            filename=filename,
            df_head=df_head.to_html(),
        )
    else:
        return jsonify({"something": "went wrong"})


@stoltzmaniac_blueprint.route("/regression/<dependent_variable>", methods=["POST"])
def regression(dependent_variable):
    file_location = request.get_data().decode("utf-8")
    file_location = file_location.split("file_location=")
    file_location = unquote(file_location[1])
    data = pd.read_csv(file_location)
    data = data.dropna()
    data = data.loc[:, data.dtypes == np.float64]
    df_final = data.copy()
    X = data.drop(columns=[dependent_variable])
    y = data[[dependent_variable]]
    model = sm.OLS(y, X).fit()
    fitted_y = model.fittedvalues
    df_final["fitted_values"] = fitted_y
    print(df_final.head())
    plots = []
    for i in X:
        bp = BasicPlot()
        p1 = bp.scatter(df_final, x_axis=i, y_axis=dependent_variable, color="black")
        p2 = bp.scatter(df_final, x_axis=i, y_axis="fitted_values", color="blue")
        plots.append(bp.plot_to_div([p1, p2]))
    return jsonify(
        {
            "pvalues": model.pvalues.to_dict(),
            "r-squared": model.rsquared,
            "plots": plots,
        }
    )
