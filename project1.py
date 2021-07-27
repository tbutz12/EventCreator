from flask import Flask, request, abort, url_for, redirect, session, render_template, flash
from models import db, User, Categories, Purchases
from datetime import datetime
from sqlalchemy import exc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project1.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

users = {}
events = []

@app.route("/")
def default():
    return redirect(url_for("login"))
    
@app.route("/login/", methods=["GET", "POST"])
def login():
    result = User.query.all()
    if "username" in session:
        return redirect(url_for("homepage", username=session["username"]))

    elif request.method == "POST":
        for r in result:
            if r.username == request.form["user"] and r.password == request.form["pass"]:
                session["username"] = r.username
                userName = r.username
                if(userName not in users):
                    users[userName] = r.password
                return redirect(url_for("homepage", username=r.username)) 
    return render_template("login.html")

@app.route("/events/", methods=["GET", "POST"])
def event():
    if "username" in session:
        eventQ = Event.query.all()
        if request.method == "POST":
            eventHost = session["username"]
            eventName = request.form["name"]
            eventDescription = request.form["des"]
            eventStartTime = request.form["stime"]
            eventEndTime = request.form["etime"]
            if(validate(eventStartTime) and validate(eventEndTime)):
                eventS = datetime.strptime(eventStartTime, '%m/%d/%Y %H:%M')
                eventE = datetime.strptime(eventEndTime, '%m/%d/%Y %H:%M')
                if (len(eventHost) == 0 | len(eventName) == 0 | len(eventDescription) == 0 | len(eventStartTime) == 0 | len(eventHost) == 0):
                    return redirect(url_for("event"))
                if(validate(eventStartTime)):
                    q = Event(eventHost, eventName, eventDescription, eventS, eventE)
                    db.session.add(q)
                    db.session.commit()
                    return redirect(url_for("homepage", username=session["username"]))
            else:
                return redirect(url_for("event"))
    return render_template("event.html", list = eventQ)

def validate(date_text):
    try:
        if date_text != datetime.strptime(date_text, "%m/%d/%Y %H:%M").strftime('%m/%d/%Y %H:%M'):
            raise ValueError
        return True
    except ValueError:
        return False

def delete_event(name = None):
    getEvent = Event.query.filter_by(eventName=name).first()
    eventID = getEvent.id
    Event.query.filter(Event.eventName == name).delete()
    user_event_junction.query.filter(user_event_junction.event_id == getEvent.id).delete()
    db.session.commit()
    return redirect(url_for("homepage", username=session["username"]))

@app.route("/event/<username>", methods=["GET", "POST"])
def homepage(username=None):
    eventQ = Event.query.all()
    junctionQ = user_event_junction.query.all()
    userQ = User.query.all()
    if not username:
        return redirect(url_for("login"))
    elif "username" in session:
        if request.method == "POST":
            button = request.form["eventName"]
            if(button[:6] == "delete"):
                eventN = button[6:]
                delete_event(eventN)
            else:
                getUser = User.query.filter_by(username=username).first()
                getEvent = Event.query.filter_by(eventName=button).first()
                getJunc = user_event_junction.query.all()
                uID = getUser.id
                query = user_event_junction(getUser.id, getEvent.id)
                db.session.add(query)
                try:
                    db.session.commit()
                except:
                    db.session.rollback()
                return redirect(url_for("homepage", username=session["username"]))
        else:
            getUser = User.query.filter_by(username=username).first()
            return render_template("eventsLogged.html", list = eventQ , user = getUser.id,  junction = junctionQ, username = session["username"])   
        return redirect(url_for("homepage", username=session["username"]))
    else:
        return render_template("homepage.html", list = eventQ)  

@app.route("/registration/", methods=["GET", "POST"])
def registration():
    if request.method == "POST":
        userName = request.form["user"]
        qUser = User.query.all()
        for u in qUser:
            users[u.username] = u.password
        if(userName in users):
            return redirect(url_for("registration"))
        users[userName] = request.form["pass"]
        if(len(userName) == 0):
            return render_template("registration.html")
        passW = request.form["pass"]
        if(len(passW) == 0):
            return render_template("registration.html")
        q = User(userName, passW)
        db.session.add(q)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("registration.html")

@app.route("/logout/")
def logout():
    if "username" in session:
        session.clear()
        return render_template("logoutPage.html")
    else:
        return redirect(url_for("login"))

app.secret_key = "asdf;lkj"
            
if __name__ == "__main__":
    app.run()

