from ..utils import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    email = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(8), unique=True, nullable=False)
    link = db.relationship('Link', backref='links', lazy=True)

    def __repr__(self):
        return f"User('{self.name}')"
    
    def save(self):
        db.session.add(self)
        db.session.commit()