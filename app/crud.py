import database as db
from app import models 

def create_user(username: str, emai: str, full_name: str, password: str):
    user = models.User(username, emai, full_name, password)
    db.session.add(user)
    db.session.commit()

    return user

def update_user(id: int, username: str, email: str, full_name: str, password: str):
    user = db.session.query(models.User).filter_by(id=id).first()

    if user is None:
        raise BaseException("404, id is invalid")
    
    if username:
        user.username = username
    if email:
        user.email = email
    if full_name:
        user.full_name = full_name
    if password:
        user.password = password

    db.session.commit()

def delete_user(id: int):
    user = db.session.query(models.User).filter_by(id=id).first()

    if user is None:
        raise BaseException("404, id is invalid")
    
    db.session.delete(user)
    db.commit()

    return user

def get_user(id: int):
    user = db.session.query(models.User).filter_by(id=id).first()

    if user is None:
        raise BaseException("404, id is invalid")
    
    return user
    
