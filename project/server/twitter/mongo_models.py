from project.server import medb


class TwitterRequest(medb.Document):
    search_term = medb.StringField(max_length=100)
    count = medb.IntField()
