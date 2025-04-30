from flask_login import UserMixin
from application import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)

    @classmethod
    def create(cls, email, password):
        return cls(email=email, password=password)

    def get_id(self):
        return str(self.id)
