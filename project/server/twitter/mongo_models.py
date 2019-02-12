from project.server import medb


class TwitterRequest(medb.Document):
    search_term = medb.StringField(max_length=100)
    count = medb.IntField()


class TwitterTimelineRequest(medb.Document):
    username = medb.StringField(max_length=100)
    image_url = medb.StringField(max_length=1000)
