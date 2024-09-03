from .database import db
from datetime import datetime
from pytz import timezone
from flask import url_for


section_books = db.Table('section_books',
    db.metadata,
    db.Column('section_id', db.Integer, db.ForeignKey('Sections.id'), primary_key=True),
    db.Column('book_id', db.Integer, db.ForeignKey('Books.id'), primary_key=True)
)

class BorrowedBooks(db.Model):
    __tablename__="BorrowedBooks"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    section = db.Column(db.String, nullable=False)
    days = db.Column(db.Integer, nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('Books.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    borrowed_date = db.Column(db.DateTime, default=datetime.now(timezone('Asia/Kolkata')))
    returned_date = db.Column(db.DateTime, nullable=True)
    returned = db.Column(db.Boolean, default=False)
    grant = db.Column(db.Boolean, default=0)
    book = db.relationship("Books", backref=db.backref("borrowed_books", lazy=True))
    user = db.relationship("Users", backref=db.backref("borrowed_books", lazy=True))
    
    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'title': self.title,
            'section': self.section,
            'days': self.days,
            'borrowed_date': self.borrowed_date,
            'grant': self.grant
        }

class Users(db.Model):
    __tablename__="Users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, unique=True, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def serialize(self):
        return {
            'email': self.email,
            'username': self.username,
            'is_admin': self.is_admin
        }

class Sections(db.Model):
    __tablename__="Sections"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    desc = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=False)
    books = db.relationship('Books', secondary=section_books, backref=db.backref('sections', lazy=True), cascade="all, delete")
    
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'desc': self.desc,
            'image': self.image,
        }

class Books(db.Model):
    __tablename__="Books"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    genre = db.Column(db.String, nullable=False)
    publisher = db.Column(db.String, nullable=False)
    desc = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=False)
    document = db.Column(db.String, nullable=True)

    
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'genre': self.genre,
            'publisher': self.publisher,
            'desc': self.desc,
            'image': self.image,
            'document': self.document,
            'document_url': url_for('static', filename=self.document, _external=True) if self.document else None
        }
    
