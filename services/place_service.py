from models import Place,Record
from database import Session
from sqlalchemy.orm import joinedload

def has_records(user_id,place_id):
    session = Session()
    try:
        return session.query(Record).filter(Record.place_id==place_id,Record.user_id==user_id).first() is not None
    finally:
        session.close()
        
def get_places(user_id, keyword=None, category_id=None):
    session = Session()
    try:
        query = session.query(Place).options(joinedload(Place.category))
        if keyword:
            query = query.filter(Place.name.like(f'%{keyword}%'))
        if category_id:
            query = query.filter(Place.category_id == int(category_id))
        return query.filter(Place.user_id==user_id).order_by(Place.id.asc()).all()
    finally:
        session.close()

def get_place(user_id,id):
    session = Session()
    try:
        return session.query(Place).filter(Place.id == id,Place.user_id == user_id).first()
    finally:
        session.close()
        
def get_place_by_name(user_id,name):
    session = Session()
    try:
        return session.query(Place).filter(Place.name==name,Place.user_id==user_id).first()
    finally:
        session.close()

def insert_place(place):
    session = Session()
    try:
        session.add(place)
        session.commit()
    finally:
        session.close()
    
def update_place(user_id,id,data):
    session = Session()
    try:
        place = session.query(Place).filter(Place.id == id,Place.user_id==user_id).first()
        if place is None or place.name == '未登録':
            return        
        for key, value in data.items():
            setattr(place, key, value)
        session.commit()
    finally:
        session.close()
        
def delete_place(user_id,id):
    if id == 1:
        return
    session = Session()
    try:
        place = session.query(Place).filter(Place.id == id,Place.user_id==user_id).first()
        if place is None or place.name == '未登録':
            return
        if place is None:
            return False
        session.delete(place)
        session.commit()
        return True
    finally:
        session.close()