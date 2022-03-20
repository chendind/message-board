from sqlalchemy import or_
from app import db
from app.models import User

def isDuplicateUser(username, email):
    return db.session.query(User.id).filter(or_(User.username == username, User.email == email)).limit(1).scalar() is not None

def addUser(username, email, password):
    user = User(username = username, email = email, password = password)
    db.session.add(user)
    db.session.commit()
    return user

def getUserByUsernameOrEmail(username, email):
    return User.query.filter(or_(User.username == username, User.email == email)).first()
