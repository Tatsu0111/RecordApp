from models import Category
from database import Session

def get_categories():
    session = Session()
    try:
        return session.query(Category).all()
    finally:
        session.close()

def get_category(id):
    session = Session()
    try:
        return session.query(Category).filter(Category.id == id).first()
    finally:
        session.close()

def insert_category(category):
    session = Session()
    try:
        session.add(category)
        session.commit()
    finally:
        session.close()
    
def update_category(id,data):
    if id == 1:
        return
    session = Session()
    try:
        category = session.query(Category).filter(Category.id == id).first()
        for key, value in data.items():
            setattr(category, key, value)
        session.commit()
    finally:
        session.close()
        
def delete_category(id):
    if id == 1:
        return
    session = Session()
    try:
        category = session.query(Category).filter(Category.id == id).first()
        if category is None:
            return False
        session.delete(category)
        session.commit()
        return True
    finally:
        session.close()