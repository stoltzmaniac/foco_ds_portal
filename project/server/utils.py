# -*- coding: utf-8 -*-
"""Helper utilities and decorators."""
import json
import datetime
import uuid
import os
import imghdr

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


class S3:
    def __init__(self):
        self.s3_session = boto3.Session(
            aws_access_key_id=BaseConfig.S3_KEY,
            aws_secret_access_key=BaseConfig.S3_SECRET,
        )
        self.bucket_name = "foco-ds-portal-files"
        self.s3_bucket = self.s3_session.resource("s3").Bucket(self.bucket_name)
        self.s3_url_prefix = f"https://s3.amazonaws.com/{self.bucket_name}/"

    def upload_file_by_name(self, file: str):
        with open(file, "r") as f:
            data = f.read()
        filename = f"{str(uuid.uuid4())}--{file}"
        upload = self.s3_bucket.put_object(Key=filename, Body=data)
        return upload

    def upload_file_by_object(self, file: os.PathLike):
        filename = f"{str(uuid.uuid4())}--{str(file.filename)}"
        upload = self.s3_bucket.put_object(Key=filename, Body=file, ACL="public-read")
        return upload, self.get_file_location(filename)

    def get_file_location(self, filename: str):
        return f"{self.s3_url_prefix}{filename}"
