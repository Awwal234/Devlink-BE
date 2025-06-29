from ..utils import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    email = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(8), unique=True, nullable=False)
    fullname = db.Column(db.String(100), nullable=True)
    link = db.relationship('Link', backref='links', lazy=True)

    def __init__(self, email, password, fullname=None):
        self.email = email
        self.password = password
        self.fullname = fullname

    def __repr__(self):
        return f"User('{self.fullname}')"

    def save(self):
        db.session.add(self)  # type: ignore
        db.session.commit()  # type: ignore