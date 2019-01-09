from flask_mongoengine.wtf import model_form
from project.server.twitter.mongo_models import TwitterRequest


TwitterForm = model_form(TwitterRequest)
