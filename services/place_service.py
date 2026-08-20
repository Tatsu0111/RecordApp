from models import Place,Record
from database import Session
from sqlalchemy.orm import joinedload

def has_records(place_id):
    session = Session()
    try:
        return session.query(Record).filter_by(place_id=place_id).first() is not None
    finally:
        session.close()
        
def get_places():
    session = Session()
    try:
        return session.query(Place).options(joinedload(Place.category)).all()
    finally:
        session.close()

def get_place(id):
    session = Session()
    try:
        return session.query(Place).filter(Place.id == id).first()
    finally:
        session.close()
        
def get_place_by_name(name):
    session = Session()
    try:
        return session.query(Place).filter_by(name=name).first()
    finally:
        session.close()

def insert_place(place):
    session = Session()
    try:
        session.add(place)
        session.commit()
    finally:
        session.close()
    
def update_place(id,data):
    if id == 1:
        return
    session = Session()
    try:
        place = session.query(Place).filter(Place.id == id).first()
        for key, value in data.items():
            setattr(place, key, value)
        session.commit()
    finally:
        session.close()
        
def delete_place(id):
    if id == 1:
        return
    session = Session()
    try:
        place = session.query(Place).filter(Place.id == id).first()
        if place is None:
            return False
        session.delete(place)
        session.commit()
        return True
    finally:
        session.close()