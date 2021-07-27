from flask_sqlalchemy import SQLAlchemy
#models
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    username = db.Column(db.String(80), unique = True)
    password = db.Column(db.String(20), unique = True)
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
            return '<User %r>' % self.username

class Categories(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    categoryName = db.Column(db.String(80), unique = False)
    amount = db.Column(db.Float, unique = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, eventHost, eventName, eventDescription, eventStartTime, eventEndTime):
        self.eventHost = eventHost
        self.eventName = eventName
        self.eventDescription = eventDescription
        self.eventStartTime = eventStartTime
        self.eventEndTime = eventEndTime
    
    def __repr__(self):
        return '<Event %r>' % self.eventName

class Purchases(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    eventHost = db.Column(db.String(80), unique = False)
    eventName = db.Column(db.String(80), unique = True)
    eventDescription = db.Column(db.String(80), unique = False)
    eventStartTime = db.Column(db.DateTime, unique = False)
    eventEndTime = db.Column(db.DateTime, unique = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, eventHost, eventName, eventDescription, eventStartTime, eventEndTime):
        self.eventHost = eventHost
        self.eventName = eventName
        self.eventDescription = eventDescription
        self.eventStartTime = eventStartTime
        self.eventEndTime = eventEndTime
    
    def __repr__(self):
        return '<Event %r>' % self.eventName
