from database import Base
from sqlalchemy import (Column, Integer, String, Text, Date, DateTime,CheckConstraint as check, ForeignKey, UniqueConstraint)
from datetime import datetime
from zoneinfo import ZoneInfo
from sqlalchemy.orm import relationship

def now_jst():
    return datetime.now(ZoneInfo("Asia/Tokyo"))

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    records = relationship('Record', back_populates='user')
    categories = relationship('Category', back_populates='user')
    places = relationship('Place', back_populates='user')

class Record(Base):
    __tablename__ = 'records'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    date = Column(Date, nullable=False)
    title = Column(String(100), default='未登録')
    category_id = Column(Integer,ForeignKey('categories.id'))
    place_id = Column(Integer,ForeignKey('places.id'))
    investment = Column(Integer, default=0)
    payout = Column(Integer, default=0)
    memo = Column(Text)
    created_at = Column(DateTime,default=now_jst,nullable=False)
    updated_at = Column(DateTime,default=now_jst,onupdate=now_jst,nullable=False)
    user = relationship('User',back_populates='records')
    category = relationship('Category',back_populates='records')
    place = relationship('Place',back_populates='records')
    __table_args__ = (
        check('investment % 10 == 0'),
        check('payout % 10 == 0'),
    )

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer,ForeignKey('users.id'),nullable=False)
    name = Column(String(50), nullable=False)
    user = relationship('User',back_populates='categories')
    records = relationship('Record',back_populates='category')
    places = relationship('Place',back_populates='category')
    __table_args__ = (UniqueConstraint('user_id','name',name='uq_categories_user_name'),)

class Place(Base):
    __tablename__ = 'places'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer,ForeignKey('users.id'),nullable=False)
    name = Column(String(50), nullable=False)
    category_id = Column(Integer,ForeignKey('categories.id'),default=1)
    user = relationship('User',back_populates='places')
    category = relationship('Category',back_populates='places')
    records = relationship('Record',back_populates='place')
    __table_args__ = (UniqueConstraint('user_id','name',name='uq_places_user_name'),)