from models import Record
from database import Session
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import joinedload

def calc_profit(investment, payout):
    return payout - investment

def get_totalProfit():
    records = get_records()
    total = 0
    for record in records:
        total += calc_profit(record.investment,record.payout)
    return total

def get_winRate():
    records = get_records()
    count = 0
    all = 0
    for record in records:
        if calc_profit(record.investment,record.payout) > 0:
            count += 1
        all += 1
    return round(count / all * 100,1)

def get_records(sort='date_desc', keyword=None, category_id=None, place_id=None, date_from=None, date_to=None):
    session = Session()
    try:
        query = session.query(Record).options(joinedload(Record.category),joinedload(Record.place))
        if keyword:
            query = query.filter(Record.title.like(f'%{keyword}%'))
            
        if category_id:
            query = query.filter(Record.category_id == int(category_id))
            
        if place_id:
            query = query.filter(Record.place_id == int(place_id))
            
        if date_from:
            date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
            query = query.filter(Record.date >= date_from)
            
        if date_to:
            date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
            query = query.filter(Record.date <= date_to)
            
        if sort == 'date_asc':
            query = query.order_by(Record.date.asc())
        elif sort == 'date_desc':
            query = query.order_by(Record.date.desc())
        elif sort == 'profit_asc':
            query = query.order_by((Record.payout - Record.investment).asc())
        elif sort == 'profit_desc':
            query = query.order_by((Record.payout - Record.investment).desc())
        elif sort == 'investment_asc':
            query = query.order_by((Record.investment).asc())
        elif sort == 'investment_desc':
            query = query.order_by((Record.investment).desc())
        
        records = query.all()
        for record in records:
            record.profit = calc_profit(record.investment, record.payout)
        return records
    finally:
        session.close()

def get_record(id):
    session = Session()
    try:
        return session.query(Record).filter(Record.id == id).first()
    finally:
        session.close()

def insert_record(record):
    session = Session()
    try:
        session.add(record)
        session.commit()
    finally:
        session.close()
    
def update_record(id,data):
    session = Session()
    try:
        record = session.query(Record).filter(Record.id == id).first()
        for key, value in data.items():
            setattr(record, key, value)
        session.commit()
    finally:
        session.close()
        
def delete_record(id):
    session = Session()
    try:
        record = session.query(Record).filter(Record.id == id).first()
        if record is None:
            return False
        session.delete(record)
        session.commit()
        return True
    finally:
        session.close()