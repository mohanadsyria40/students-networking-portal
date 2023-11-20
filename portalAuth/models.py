from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Student(db.Model, UserMixin):
    studentId = db.Column(db.String(10), primary_key=True)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(20), unique=True, nullable=False)
    threads = db.relationship('Thread')
    profile = db.relationship('Profile', uselist=False)
    posts = db.relationship('Post')
    
    
class Thread(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    studentId = db.Column(db.String(10), db.ForeignKey('student.studentId'), unique=True, nullable=False)
    title = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime(timezone=True), default=func.now())
    posts = db.relationship('Post')
    
    
class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    grade = db.Column(db.Decimal(precision=3, scale=2))
    description = db.Column(db.Text)
    studentId = db.Column(db.String(10), db.ForeignKey('student.studentId'), nullable=False)
    
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    studentId = db.Column(db.String(10), db.ForeignKey('student.studentId'), unique=True, nullable=False)
    threadId = db.Column(db.Integer, db.ForeignKey('thread.id'), nullable=False)
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime(timezone=True), default=func.now())
    
    
class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    
    