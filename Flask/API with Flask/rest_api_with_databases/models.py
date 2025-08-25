from app import db

class Puppy(db.Model):
    name = db.Column(db.String(80), primary_key = True)     #Other fields could be added as well

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'name' : self.name}