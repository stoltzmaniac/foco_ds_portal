# -*- coding: utf-8 -*-
"""Helper utilities and decorators."""
import json
import datetime

# from bson.objectid import ObjectId
from flask import flash
import twitter
import boto3

from project.server.config import BaseConfig


def flash_errors(form, category="warning"):
    """Flash all errors for a form."""
    for field, errors in form.errors.items():
        for error in errors:
            flash("{0} - {1}".format(getattr(form, field).label.text, error), category)


# class JSONEncoder(json.JSONEncoder):
#     """ extend json-encoder class"""
#
#     def default(self, o):
#         if isinstance(o, ObjectId):
#             return str(o)
#         if isinstance(o, datetime.datetime):
#             return str(o)
#         return json.JSONEncoder.default(self, o)


twtr = twitter.Api(
    consumer_key=BaseConfig.TWTR_CONSUMER_KEY,
    consumer_secret=BaseConfig.TWTR_CONSUMER_SECRET,
    access_token_key=BaseConfig.TWTR_TOKEN_KEY,
    access_token_secret=BaseConfig.TWTR_TOKEN_SECRET,
)

s3_session = boto3.Session(
    aws_access_key_id=BaseConfig.S3_KEY,
    aws_secret_access_key=BaseConfig.S3_SECRET
)

s3 = s3_session.resource('s3').Bucket('foco-ds-portal-files')
