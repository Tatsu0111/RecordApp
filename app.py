from flask import Flask, render_template as rt, request, redirect,url_for, flash
import services.record_service as rs
import services.place_service as ps
import services.category_service as cs
import services.analysis_service as anas
import services.graph_service as gs
import services.uranai_service as us
from models import Record, Place, Category
from datetime import datetime
from forms import RecordForm, PlaceForm, CategoryForm
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

@app.route('/')
def index():
    return rt('index.html',total = rs.get_totalProfit(),win=rs.get_winRate(),recovery=rs.get_recoveryRate(),monthly_top3=rs.get_monthly_top3())

#占い
@app.route('/uranai', methods=['GET','POST'])
def uranai():
    result = us.draw_fortune()
    return rt('uranai/uranai.html',name=result[0],icon=result[1])

#収支
@app.route('/records')
def show_records():
    allowed_sorts = [
        'date_desc',
        'date_asc',
        'investment_desc',
        'investment_asc',
        'profit_desc',
        'profit_asc',
        'recovery_desc',
        'recovery_asc'
    ]
    sort = request.args.get('sort', 'date_desc')
    if sort not in allowed_sorts:
        sort = 'date_desc'
    title_keyword = request.args.get('title_keyword', '')
    category_id = request.args.get('category_id')
    place_id = request.args.get('place_id')
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    memo_keyword = request.args.get('memo_keyword', '')
    if not anas.validate_date_range(date_from, date_to):
        flash('開始日は終了日より前の日付にしてください', 'fail')
        date_from = ''
        date_to = ''
    records = rs.get_records(sort,title_keyword,category_id,place_id,date_from,date_to,memo_keyword)
    return rt('records/list.html', records=records, sort=sort, title_keyword=title_keyword, category_id=category_id, place_id=place_id, date_from=date_from, date_to=date_to, memo_keyword=memo_keyword, categories=cs.get_categories(),places=ps.get_places())

@app.route('/records/add', methods=['GET','POST'])
@app.route('/records/<int:id>/edit', methods=['GET','POST'])
def record_form(id=None):
    row = None if id is None else rs.get_record(id)
    form = RecordForm(obj=row)
    form.category_id.choices = [(c.id, c.name)for c in cs.get_categories()]
    form.place_id.choices = [(p.id, p.name)for p in ps.get_places()]
    if form.validate_on_submit():
        data = {
            'date': form.date.data,
            'title': form.title.data or '未登録',
            'category_id': form.category_id.data,
            'place_id': form.place_id.data,
            'investment': form.investment.data or 0,
            'payout': form.payout.data or 0,
            'memo': form.memo.data
        }
        if id is None:
            record = Record(**data)
            rs.insert_record(record)
            flash('収支を登録しました', 'success')
        else:
            rs.update_record(id, data)
            flash('収支を修正しました', 'success')
        return redirect(url_for('show_records'))
    return rt('records/form.html',form=form,row=row)

@app.route('/records/<int:id>/delete',methods=['POST'])
def record_delete(id):
    rs.delete_record(id)
    flash('収支を削除しました', 'success')
    return redirect(url_for('show_records'))

#分析
@app.route('/analysis')
def record_analyze():
    return rt('analyze/index.html')

@app.route('/analysis/lifetime')
def analysis_lifetime():
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    if not anas.validate_date_range(date_from, date_to):
        flash('開始日は終了日より前の日付にしてください', 'fail')
        date_from = ''
        date_to = ''
    summary = anas.get_lifetime_summary(date_from, date_to)
    data = anas.get_lifetime_graph_data(date_from, date_to)
    fig = gs.create_lifetime_graph(data)
    graph = fig.to_html(full_html=False)
    return rt('analyze/lifetime.html', summary=summary, date_from=date_from, date_to=date_to, graph=graph)

@app.route('/analysis/year')
def analysis_year():
    summary = anas.get_yearly_summary()
    fig = gs.create_yearly_graph(summary)
    graph = fig.to_html(full_html=False)
    return rt('analyze/year.html', summary=summary, graph=graph)

@app.route('/analysis/month')
def analysis_month():
    selected_year = request.args.get('year', '')
    years = anas.get_years()
    summary = anas.get_monthly_summary(selected_year)
    fig = gs.create_monthly_graph(summary)
    graph = fig.to_html(full_html=False)
    return rt('analyze/month.html', years=years, selected_year=selected_year, summary=summary, graph=graph)

@app.route('/analysis/day')
def analysis_day():
    selected_year = request.args.get('year', '')
    selected_month = request.args.get('month', '')
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    if not anas.validate_date_range(date_from, date_to):
        flash('開始日は終了日より前の日付にしてください', 'fail')
        date_from = ''
        date_to = ''
    years = anas.get_years()
    months = anas.get_months()
    summary = anas.get_daily_summary(selected_year, selected_month, date_from, date_to)
    fig = gs.create_daily_graph(summary)
    graph = fig.to_html(full_html=False)
    return rt('analyze/day.html', years=years, selected_year=selected_year, months=months, selected_month=selected_month, date_from=date_from, date_to=date_to, summary=summary, graph=graph)

@app.route('/analysis/place')
def analysis_place():
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    if not anas.validate_date_range(date_from, date_to):
        flash('開始日は終了日より前の日付にしてください', 'fail')
        date_from = ''
        date_to = ''
    summary = anas.get_place_summary(date_from, date_to)
    fig = gs.create_place_graph(summary)
    graph = fig.to_html(full_html=False)
    return rt('analyze/place.html', summary=summary, date_from=date_from, date_to=date_to, graph=graph)

@app.route('/analysis/category')
def analysis_category():
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    if not anas.validate_date_range(date_from, date_to):
        flash('開始日は終了日より前の日付にしてください', 'fail')
        date_from = ''
        date_to = ''
    summary = anas.get_category_summary(date_from, date_to)
    fig = gs.create_category_graph(summary)
    graph = fig.to_html(full_html=False)
    return rt('analyze/category.html', summary=summary, date_from=date_from, date_to=date_to, graph=graph)

#場所
@app.route('/places')
def place_master():
    keyword = request.args.get('keyword', '')
    category_id = request.args.get('category_id')
    places = ps.get_places(keyword, category_id)
    return rt('places/list.html', keyword=keyword, category_id=category_id, places=places, categories=cs.get_categories())

@app.route('/places/add', methods=['GET','POST'])
@app.route('/places/<int:id>/edit', methods=['GET','POST'])
def place_form(id=None):
    row = None if id is None else ps.get_place(id)
    form = PlaceForm(obj=row)
    form.category_id.choices = [(c.id, c.name)for c in cs.get_categories()]
    if form.validate_on_submit():
        place = ps.get_place_by_name(form.name.data)
        if place is not None and place.id != id:
            form.name.errors.append('この場所はすでに登録されています')
        else:
            data = {
                'name': form.name.data,
                'category_id': form.category_id.data
            }
            if id is None:
                place = Place(**data)
                ps.insert_place(place)
                flash('場所を登録しました', 'success')
            else:
                ps.update_place(id, data)
                flash('場所を修正しました', 'success')
            return redirect(url_for('place_master'))
    return rt('places/form.html',form=form,row=row)

@app.route('/places/<int:id>/delete', methods=['POST'])
def place_delete(id):
    if id == 1:
        flash('この項目は削除できません', 'fail')
    elif ps.has_records(id):
        flash('この場所は収支で使用されているため削除できません', 'fail')
    else:
        ps.delete_place(id)
        flash('場所を削除しました', 'success')
    return redirect(url_for('place_master'))

#カテゴリ
@app.route('/categories')
def category_master():
    return rt('categories/list.html', categories = cs.get_categories())

@app.route('/categories/add', methods=['GET','POST'])
@app.route('/categories/<int:id>/edit', methods=['GET','POST'])
def category_form(id=None):
    row = None if id is None else cs.get_category(id)
    form = CategoryForm(obj=row)
    if form.validate_on_submit():
        category = cs.get_category_by_name(form.name.data)
        if category is not None and category.id != id:
            form.name.errors.append('このカテゴリはすでに登録されています')
        else:
            data = {
                'name': form.name.data
            }
            if id is None:
                category = Category(**data)
                cs.insert_category(category)
                flash('カテゴリを登録しました', 'success')
            else:
                cs.update_category(id, data)
                flash('カテゴリを修正しました', 'success')
            return redirect(url_for('category_master'))
    return rt('categories/form.html',form=form,row=row)

@app.route('/categories/<int:id>/delete', methods=['POST'])
def category_delete(id):
    if id == 1:
        flash('この項目は削除できません', 'fail')
    elif cs.has_records(id):
        flash('このカテゴリは収支で使用されているため削除できません', 'fail')
    elif cs.has_places(id):
        flash('このカテゴリは場所で使用されているため削除できません', 'fail')
    else:
        cs.delete_category(id)
        flash('カテゴリを削除しました', 'success')
    return redirect(url_for('category_master'))

if __name__ == '__main__':
    app.run(debug=True)