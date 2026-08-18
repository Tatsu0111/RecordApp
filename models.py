from database import Base
from sqlalchemy import Column, Integer, String, Text,Date, DateTime, func, CheckConstraint as check, ForeignKey
from datetime import datetime
from zoneinfo import ZoneInfo
from sqlalchemy.orm import relationship

def now_jst():
    return datetime.now(ZoneInfo("Asia/Tokyo"))

class Record(Base):
    __tablename__ = 'records'
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    title = Column(String(100), default='未登録')
    category_id = Column(Integer, ForeignKey('categories.id'), default=1)
    place_id = Column(Integer, ForeignKey('places.id'), default=1)
    investment = Column(Integer, default=0)
    payout = Column(Integer, default=0)
    memo = Column(Text)
    created_at = Column(DateTime, default=now_jst, nullable=False)
    updated_at = Column(DateTime, default=now_jst, onupdate=now_jst, nullable=False)
    category = relationship("Category", back_populates="records")
    place = relationship("Place", back_populates="records")
    __table_args__ = (
        check('investment % 10 == 0'),
        check("payout % 10 == 0"),
    )
    
class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    records = relationship("Record", back_populates="category")
    places = relationship("Place", back_populates="category")
    
class Place(Base):
    __tablename__ = 'places'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    category_id = Column(Integer, ForeignKey("categories.id"), default=1)
    records = relationship("Record", back_populates="place")
    category = relationship("Category", back_populates="places")