from models import Category,Record,Place
from database import Session
from sqlalchemy import func,case,extract
from services.record_service import calc_profit, calc_recoveryRate, calc_winRate
from datetime import datetime

def validate_date_range(date_from, date_to):
    if date_from and date_to and date_from > date_to:
        return False
    return True

def get_years(user_id):
    session = Session()
    try:
        return [str(int(row[0])) for row in session.query(extract('year', Record.date)).filter(Record.user_id==user_id).distinct().order_by(extract('year', Record.date).desc()).all()]
    finally:
        session.close()

def get_months(user_id):
    session = Session()
    try:
        return [f'{int(row[0]):02d}' for row in session.query(extract('month', Record.date)).filter(Record.user_id==user_id).distinct().order_by(extract('month', Record.date).desc()).all()]
    finally:
        session.close()

def get_summary_columns():
    return [
        func.sum(Record.investment).label('investment'),
        func.sum(Record.payout).label('payout'),
        func.count(Record.id).label('count'),
        func.sum(case((Record.payout > Record.investment, 1), else_=0)).label('win'),
        func.sum(case((Record.payout < Record.investment, 1), else_=0)).label('lose'),
        func.sum(case((Record.payout == Record.investment, 1), else_=0)).label('even')
    ]

def make_summary(result, key_name):
    summary = []
    for row in result:
        profit = calc_profit(row.investment, row.payout)
        win_rate = calc_winRate(row.win, row.count)
        recovery = calc_recoveryRate(row.investment, row.payout)
        summary.append({
            key_name: row[0],
            'count': row.count,
            'win': row.win,
            'lose': row.lose,
            'even': row.even,
            'win_rate': win_rate,
            'investment': row.investment,
            'payout': row.payout,
            'profit': profit,
            'recovery': recovery
        })
    return summary

def get_lifetime_summary(user_id, date_from=None, date_to=None):
    session = Session()
    try:
        query = session.query(*get_summary_columns()).filter(Record.user_id==user_id)
        if date_from:
            date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
            query = query.filter(Record.date >= date_from)
        if date_to:
            date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
            query = query.filter(Record.date <= date_to)
        row = query.one()
        profit = calc_profit(row.investment, row.payout)
        win_rate = calc_winRate(row.win, row.count)
        recovery = calc_recoveryRate(row.investment, row.payout)
        return {
            'count': row.count,
            'win': row.win,
            'lose': row.lose,
            'even': row.even,
            'win_rate': win_rate,
            'investment': row.investment,
            'payout': row.payout,
            'profit': profit,
            'recovery': recovery
        }
    finally:
        session.close()

def get_lifetime_graph_data(user_id, date_from=None, date_to=None):
    session = Session()
    try:
        query = session.query(Record.date, func.sum(Record.payout - Record.investment).label('profit')).filter(Record.user_id==user_id)
        if date_from:
            date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
            query = query.filter(Record.date >= date_from)
        if date_to:
            date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
            query = query.filter(Record.date <= date_to)
        result = query.group_by(Record.date).order_by(Record.date).all()
        return [{'date': row.date.strftime('%Y-%m-%d'), 'profit': row.profit}for row in result]
    finally:
        session.close()

def get_yearly_summary(user_id):
    session = Session()
    try:
        year = extract('year', Record.date)
        result = session.query(year, *get_summary_columns()).filter(Record.user_id==user_id).group_by(year).all()
        summary = make_summary(result, 'year')
        for row in summary:
            row['year'] = str(int(row['year']))
        return summary
    finally:
        session.close()
    
def get_monthly_summary(user_id, year=None):
    session = Session()
    try:
        ym = (extract('year', Record.date) * 100 + extract('month', Record.date))
        query = session.query(ym, *get_summary_columns()).filter(Record.user_id==user_id)
        if year:
            query = query.filter(extract('year', Record.date) == int(year))
        result = query.group_by(ym).all()
        summary = make_summary(result, 'ym')
        for row in summary:
            ym = int(row['ym'])
            row['ym'] = f'{ym // 100:04d}-{ym % 100:02d}'
        return summary
    finally:
        session.close()
        
def get_daily_summary(user_id, year=None, month=None, date_from=None, date_to=None):
    session = Session()
    try:
        ymd = Record.date
        query = session.query(ymd, *get_summary_columns()).filter(Record.user_id==user_id)
        if year:
            query = query.filter(extract('year', Record.date) == int(year))
        if month:
            query = query.filter(extract('month', Record.date) == int(month))
            
        if date_from:
            date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
            query = query.filter(Record.date >= date_from)            
        if date_to:
            date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
            query = query.filter(Record.date <= date_to)
            
        result = query.group_by(ymd).all()
        summary = make_summary(result, 'ymd')
        for row in summary:
            row['ymd'] = row['ymd'].strftime('%Y-%m-%d')
        return summary
    finally:
        session.close()
    
def get_place_summary(user_id, date_from=None, date_to=None):
    session = Session()
    try:
        query = session.query(Place.name, *get_summary_columns()).join(Place, Record.place_id == Place.id).filter(Record.user_id==user_id)
        if date_from:
            date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
            query = query.filter(Record.date >= date_from)            
        if date_to:
            date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
            query = query.filter(Record.date <= date_to)
        result = query.group_by(Record.place_id, Place.name).all()
        return make_summary(result, 'place')
    finally:
        session.close()
    
def get_category_summary(user_id, date_from=None, date_to=None):
    session = Session()
    try:
        query = session.query(Category.name, *get_summary_columns()).join(Category, Record.category_id == Category.id).filter(Record.user_id==user_id)
        if date_from:
            date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
            query = query.filter(Record.date >= date_from)            
        if date_to:
            date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
            query = query.filter(Record.date <= date_to)
        result = query.group_by(Record.category_id, Category.name).all()
        return make_summary(result, 'category')
    finally:
        session.close()