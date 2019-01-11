from flask_mongoengine.wtf import model_form
from project.server.twitter.mongo_models import TwitterRequest, TwitterTimelineRequest


TwitterForm = model_form(TwitterRequest)
TwitterTimelineForm = model_form(TwitterTimelineRequest)

