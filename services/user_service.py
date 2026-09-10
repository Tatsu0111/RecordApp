from werkzeug.security import generate_password_hash, check_password_hash
from database import Session
from models import User

def insert_user(name, password):
    session = Session()
    try:
        user = User(name=name,password_hash=generate_password_hash(password))
        session.add(user)
        session.commit()
        return user.id
    finally:
        session.close()
        
def get_user(user_id):
    session = Session()
    try:
        return session.query(User).filter(User.id == user_id).first()
    finally:
        session.close()
        
def get_user_by_name(name):
    session = Session()
    try:
        return session.query(User).filter(User.name == name).first()
    finally:
        session.close()
        
def check_password(user, password):
    return check_password_hash(user.password_hash,password)