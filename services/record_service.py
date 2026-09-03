from models import Record
from database import Session
from datetime import datetime
from zoneinfo import ZoneInfo
from sqlalchemy import func
from sqlalchemy.orm import joinedload

def calc_profit(investment, payout):
    return payout - investment

def calc_winRate(win, count):
    if count == 0:
        return 0.0
    return round((win / count) * 100, 1)

def calc_recoveryRate(investment, payout):
    if investment == 0:
        return 0.0
    return round((payout / investment) * 100, 1)

def get_recoveryRate():
    records = get_records()
    total_investment = sum(record.investment for record in records)
    total_payout = sum(record.payout for record in records)
    return calc_recoveryRate(total_investment, total_payout)

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
    return calc_winRate(count, all)

def get_monthly_top3():
    session = Session()
    try:
        now_jst = datetime.now(ZoneInfo('Asia/Tokyo'))
        today = now_jst.date()
        records = (session.query(Record).filter(func.strftime('%Y-%m', Record.date)== today.strftime('%Y-%m')).all())
        summary = []
        for record in records:
            profit = calc_profit(record.investment, record.payout)
            recovery_rate = calc_recoveryRate(record.investment, record.payout)
            summary.append({
                'title': record.title,
                'recovery_rate': recovery_rate,
                'profit': profit
            })
        summary.sort(key=lambda x: x['recovery_rate'],reverse=True)
        return summary[:3]
    finally:
        session.close()

def get_records(sort='date_desc', title_keyword=None, category_id=None, place_id=None, date_from=None, date_to=None, memo_keyword=None):
    session = Session()
    try:
        query = session.query(Record).options(joinedload(Record.category),joinedload(Record.place))
        if title_keyword:
            query = query.filter(Record.title.like(f'%{title_keyword}%'))
            
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
            
        if memo_keyword:
            query = query.filter(Record.memo.like(f'%{memo_keyword}%'))
            
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
        elif sort == 'recovery_asc':
            query = query.order_by((Record.payout / Record.investment * 100).asc())
        elif sort == 'recovery_desc':
            query = query.order_by((Record.payout / Record.investment * 100).desc())
        
        records = query.all()
        for record in records:
            record.profit = calc_profit(record.investment, record.payout)
            record.recovery = calc_recoveryRate(record.investment, record.payout)
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