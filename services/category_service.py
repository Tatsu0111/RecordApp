from models import Category,Record,Place
from database import Session

def has_records(user_id,category_id):
    session = Session()
    try:
        return session.query(Record).filter(Record.category_id==category_id,Record.user_id==user_id).first() is not None
    finally:
        session.close()
        
def has_places(user_id,category_id):
    session = Session()
    try:
        return session.query(Place).filter(Place.category_id==category_id,Place.user_id==user_id).first() is not None
    finally:
        session.close()

def get_categories(user_id):
    session = Session()
    try:
        return session.query(Category).filter(Category.user_id==user_id).order_by(Category.id.asc()).all()
    finally:
        session.close()

def get_category(user_id,id):
    session = Session()
    try:
        return session.query(Category).filter(Category.id == id,Category.user_id == user_id).first()
    finally:
        session.close()
        
def get_category_by_name(user_id,name):
    session = Session()
    try:
        return session.query(Category).filter(Category.name==name,Category.user_id==user_id).first()
    finally:
        session.close()

def insert_category(category):
    session = Session()
    try:
        session.add(category)
        session.commit()
        return category.id
    finally:
        session.close()
    
def update_category(user_id,id,data):
    session = Session()
    try:
        category = session.query(Category).filter(Category.id == id,Category.user_id == user_id).first()
        if category is None or category.name == '未登録':
            return
        for key, value in data.items():
            setattr(category, key, value)
        session.commit()
    finally:
        session.close()
        
def delete_category(user_id,id):
    session = Session()
    try:
        category = session.query(Category).filter(Category.id == id,Category.user_id == user_id).first()
        if category is None or category.name == '未登録':
            return
        if category is None:
            return False
        session.delete(category)
        session.commit()
        return True
    finally:
        session.close()