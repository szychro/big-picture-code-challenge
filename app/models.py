from . import db

class Book(db.Model):
    isbn_13 = db.Column(db.String(13), primary_key=True, unique=True, nullable=False)
    isbn_10 = db.Column(db.String(10), unique=True)
    author = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    summary = db.Column(db.String(1000))
    cover = db.Column(db.String(300))