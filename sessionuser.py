from flask_login import *

class Sessionuser(UserMixin):
    def __init__(self):
        self.id = "yolo"

    def __init__(self, id):
        self.id = id
