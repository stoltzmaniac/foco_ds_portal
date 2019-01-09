import time
from urllib.parse import quote_plus

from flask import jsonify

from onehundreddaysofcode.utils import twtr


def twitter_search(request) -> list:
    form_data = request.form
    search_query = (
        f"q={quote_plus(form_data['search_term'])}&count={str(form_data['count'])}"
    )
    results = twtr.GetSearch(raw_query=search_query)
    data = []
    for r in results:
        d = r.AsDict()
        d["timestamp"] = time.strftime(
            "%Y-%m-%d %H:%M:%S",
            time.strptime(d["created_at"], "%a %b %d %H:%M:%S +0000 %Y"),
        )
        data.append(d)
    return data
