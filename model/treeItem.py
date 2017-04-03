from mongoengine import *


class TreeList(Document):
    src = StringField()
    title = StringField()
    description = StringField()
    image = FileField()


