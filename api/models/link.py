from ..utils import db

class Link(db.Model):
    __tablename__ = 'link'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    platform = db.Column(db.String(30), nullable=False)
    link = db.Column(db.String(), nullable=False)
    user = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return f"Link('{self.link}')"
    
    def save(self):
        db.session.add(self)
        db.session.commit()