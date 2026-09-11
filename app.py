from flask import Flask, render_template as rt, request, redirect,url_for, flash, session
import services.record_service as rs
import services.place_service as ps
import services.category_service as cs
import services.analysis_service as anas
import services.graph_service as gs
import services.uranai_service as us
import services.user_service as users
from models import Record, Place, Category
from datetime import datetime
from forms import UserForm, RecordForm, PlaceForm, CategoryForm
from dotenv import load_dotenv
import os
from database import Base, engine

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
Base.metadata.create_all(engine)

@app.route('/')
def auth():
    return rt('auth.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = UserForm()
    if form.validate_on_submit():
        if users.get_user_by_name(form.name.data):
            flash('そのアカウント名は既に使用されています', 'error')
        else:
            user_id = users.insert_user(form.name.data,form.password.data)
            category = Category(user_id=user_id,name='未登録')
            category_id = cs.insert_category(category)
            place = Place(user_id=user_id,name='未登録',category_id=category_id)
            ps.insert_place(place)
            session["user_id"] = user_id
            flash('アカウントを登録しました', 'success')
            return redirect(url_for('login'))
    return rt('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = UserForm()
    if form.validate_on_submit():
        user = users.get_user_by_name(form.name.data)
        if user and users.check_password(user, form.password.data):
            session["user_id"] = user.id
            flash('ログインしました', 'success')
            return redirect(url_for('index'))
        flash('アカウント名またはパスワードが違います', 'error')
    return rt('login.html', form=form)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('ログアウトしました', 'success')
    return redirect(url_for('auth'))

@app.route('/top')
def index():
    if 'user_id' not in session:
        flash('ログインしてください','fail')
        return redirect(url_for('auth'))
    user_id = session['user_id']
    user = users.get_user(user_id)
    return rt('index.html',username=user.name,total = rs.get_totalProfit(user_id),win=rs.get_winRate(user_id),recovery=rs.get_recoveryRate(user_id),monthly_top3=rs.get_monthly_top3(user_id))

#占い
@app.route('/uranai', methods=['GET','POST'])
def uranai():
    result = us.draw_fortune()
    return rt('uranai/uranai.html',name=result[0],icon=result[1])

#収支
@app.route('/records')
def show_records():
    if 'user_id' not in session:
        flash('ログインしてください','fail')
        return redirect(url_for('auth'))
    user_id = session['user_id']
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
    records = rs.get_records(user_id,sort,title_keyword,category_id,place_id,date_from,date_to,memo_keyword)
    return rt('records/list.html', records=records, sort=sort, title_keyword=title_keyword, category_id=category_id, place_id=place_id, date_from=date_from, date_to=date_to, memo_keyword=memo_keyword, categories=cs.get_categories(user_id),places=ps.get_places(user_id))

@app.route('/records/add', methods=['GET','POST'])
@app.route('/records/<int:id>/edit', methods=['GET','POST'])
def record_form(id=None):
    if 'user_id' not in session:
        flash('ログインしてください','fail')
        return redirect(url_for('auth'))
    user_id = session["user_id"]
    row = None if id is None else rs.get_record(user_id,id)
    if id is not None and row is None:
        return rt('errors/404.html'),404
    form = RecordForm(obj=row)
    form.category_id.choices = [(c.id, c.name)for c in cs.get_categories(user_id)]
    form.place_id.choices = [(p.id, p.name)for p in ps.get_places(user_id)]
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
            record = Record(user_id=user_id, **data)
            rs.insert_record(record)
            flash('収支を登録しました', 'success')
        else:
            rs.update_record(user_id, id, data)
            flash('収支を修正しました', 'success')
        return redirect(url_for('show_records'))
    return rt('records/form.html',form=form,row=row)

@app.route('/records/<int:id>/delete',methods=['POST'])
def record_delete(id):
    if 'user_id' not in session:
        flash('ログインしてください','fail')
        return redirect(url_for('auth'))
    user_id = session['user_id']
    rs.delete_record(user_id, id)
    flash('収支を削除しました', 'success')
    return redirect(url_for('show_records'))

#分析
@app.route('/analysis')
def record_analyze():
    if 'user_id' not in session:
        flash('ログインしてください','fail')
        return redirect(url_for('auth'))
    return rt('analyze/index.html')

@app.route('/analysis/lifetime')
def analysis_lifetime():
    if 'user_id' not in session:
        flash('ログインしてください','fail')
        return redirect(url_for('auth'))
    user_id = session['user_id']
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    if not anas.validate_date_range(date_from, date_to):
        flash('開始日は終了日より前の日付にしてください', 'fail')
        date_from = ''
        date_to = ''
    summary = anas.get_lifetime_summary(user_id, date_from, date_to)
    data = anas.get_lifetime_graph_data(user_id, date_from, date_to)
    fig = gs.create_lifetime_graph(data)
    graph = fig.to_html(full_html=False)
    return rt('analyze/lifetime.html', summary=summary, date_from=date_from, date_to=date_to, graph=graph)

@app.route('/analysis/year')
def analysis_year():
    if 'user_id' not in session:
        flash('ログインしてください','fail')
        return redirect(url_for('auth'))
    user_id = session['user_id']
    summary = anas.get_yearly_summary(user_id)
    fig = gs.create_yearly_graph(summary)
    graph = fig.to_html(full_html=False)
    return rt('analyze/year.html', summary=summary, graph=graph)

@app.route('/analysis/month')
def analysis_month():
    if 'user_id' not in session:
        flash('ログインしてください','fail')
        return redirect(url_for('auth'))
    user_id = session['user_id']
    selected_year = request.args.get('year', '')
    years = anas.get_years(user_id)
    summary = anas.get_monthly_summary(user_id, selected_year)
    fig = gs.create_monthly_graph(summary)
    graph = fig.to_html(full_html=False)
    return rt('analyze/month.html', years=years, selected_year=selected_year, summary=summary, graph=graph)

@app.route('/analysis/day')
def analysis_day():
    if 'user_id' not in session:
        flash('ログインしてください','fail')
        return redirect(url_for('auth'))
    user_id = session['user_id']
    selected_year = request.args.get('year', '')
    selected_month = request.args.get('month', '')
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    if not anas.validate_date_range(date_from, date_to):
        flash('開始日は終了日より前の日付にしてください', 'fail')
        date_from = ''
        date_to = ''
    years = anas.get_years(user_id)
    months = anas.get_months(user_id)
    summary = anas.get_daily_summary(user_id, selected_year, selected_month, date_from, date_to)
    fig = gs.create_daily_graph(summary)
    graph = fig.to_html(full_html=False)
    return rt('analyze/day.html', years=years, selected_year=selected_year, months=months, selected_month=selected_month, date_from=date_from, date_to=date_to, summary=summary, graph=graph)

@app.route('/analysis/place')
def analysis_place():
    if 'user_id' not in session:
        flash('ログインしてください','fail')
        return redirect(url_for('auth'))
    user_id = session['user_id']
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    if not anas.validate_date_range(date_from, date_to):
        flash('開始日は終了日より前の日付にしてください', 'fail')
        date_from = ''
        date_to = ''
    summary = anas.get_place_summary(user_id, date_from, date_to)
    fig = gs.create_place_graph(summary)
    graph = fig.to_html(full_html=False)
    return rt('analyze/place.html', summary=summary, date_from=date_from, date_to=date_to, graph=graph)

@app.route('/analysis/category')
def analysis_category():
    if 'user_id' not in session:
        flash('ログインしてください','fail')
        return redirect(url_for('auth'))
    user_id = session['user_id']
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    if not anas.validate_date_range(date_from, date_to):
        flash('開始日は終了日より前の日付にしてください', 'fail')
        date_from = ''
        date_to = ''
    summary = anas.get_category_summary(user_id, date_from, date_to)
    fig = gs.create_category_graph(summary)
    graph = fig.to_html(full_html=False)
    return rt('analyze/category.html', summary=summary, date_from=date_from, date_to=date_to, graph=graph)

#場所
@app.route('/places')
def place_master():
    if 'user_id' not in session:
        flash('ログインしてください','fail')
        return redirect(url_for('auth'))
    user_id = session['user_id']
    keyword = request.args.get('keyword', '')
    category_id = request.args.get('category_id')
    places = ps.get_places(user_id, keyword, category_id)
    return rt('places/list.html', keyword=keyword, category_id=category_id, places=places, categories=cs.get_categories(user_id))

@app.route('/places/add', methods=['GET','POST'])
@app.route('/places/<int:id>/edit', methods=['GET','POST'])
def place_form(id=None):
    if 'user_id' not in session:
        flash('ログインしてください','fail')
        return redirect(url_for('auth'))
    user_id = session["user_id"]
    row = None if id is None else ps.get_place(user_id,id)
    if id is not None and row is None:
        return rt('errors/404.html'),404
    form = PlaceForm(obj=row)
    form.category_id.choices = [(c.id, c.name)for c in cs.get_categories(user_id)]
    if form.validate_on_submit():
        place = ps.get_place_by_name(user_id,form.name.data)
        if place is not None and place.id != id:
            form.name.errors.append('この場所はすでに登録されています')
        else:
            data = {
                'name': form.name.data,
                'category_id': form.category_id.data
            }
            if id is None:
                place = Place(user_id=user_id,**data)
                ps.insert_place(place)
                flash('場所を登録しました', 'success')
            elif row.name == '未登録':
                flash('この項目は修正できません', 'fail')
            else:
                ps.update_place(user_id, id, data)
                flash('場所を修正しました', 'success')
            return redirect(url_for('place_master'))
    return rt('places/form.html',form=form,row=row)

@app.route('/places/<int:id>/delete', methods=['POST'])
def place_delete(id):
    if 'user_id' not in session:
        flash('ログインしてください','fail')
        return redirect(url_for('auth'))
    user_id = session['user_id']
    place = ps.get_place(user_id, id)
    if place.name == '未登録':
        flash('この項目は削除できません', 'fail')
    elif ps.has_records(user_id,id):
        flash('この場所は収支で使用されているため削除できません', 'fail')
    else:
        ps.delete_place(user_id,id)
        flash('場所を削除しました', 'success')
    return redirect(url_for('place_master'))

#カテゴリ
@app.route('/categories')
def category_master():
    if 'user_id' not in session:
        flash('ログインしてください','fail')
        return redirect(url_for('auth'))
    user_id = session["user_id"]
    return rt('categories/list.html', categories = cs.get_categories(user_id))

@app.route('/categories/add', methods=['GET','POST'])
@app.route('/categories/<int:id>/edit', methods=['GET','POST'])
def category_form(id=None):
    if 'user_id' not in session:
        flash('ログインしてください','fail')
        return redirect(url_for('auth'))
    user_id = session["user_id"]
    row = None if id is None else cs.get_category(user_id,id)
    if id is not None and row is None:
        return rt('errors/404.html'),404
    form = CategoryForm(obj=row)
    if form.validate_on_submit():
        category = cs.get_category_by_name(user_id,form.name.data)
        if category is not None and category.id != id:
            form.name.errors.append('このカテゴリはすでに登録されています')
        else:
            data = {
                'name': form.name.data
            }
            if id is None:
                category = Category(user_id=user_id,**data)
                cs.insert_category(category)
                flash('カテゴリを登録しました', 'success')
            elif row.name == '未登録':
                flash('この項目は修正できません', 'fail')
            else:
                cs.update_category(user_id, id, data)
                flash('カテゴリを修正しました', 'success')
            return redirect(url_for('category_master'))
    return rt('categories/form.html',form=form,row=row)

@app.route('/categories/<int:id>/delete', methods=['POST'])
def category_delete(id):
    if 'user_id' not in session:
        flash('ログインしてください','fail')
        return redirect(url_for('auth'))
    user_id = session["user_id"]
    if Category.name == '未登録':
        flash('この項目は削除できません', 'fail')
    elif cs.has_records(user_id,id):
        flash('このカテゴリは収支で使用されているため削除できません', 'fail')
    elif cs.has_places(user_id,id):
        flash('このカテゴリは場所で使用されているため削除できません', 'fail')
    else:
        cs.delete_category(user_id,id)
        flash('カテゴリを削除しました', 'success')
    return redirect(url_for('category_master'))

# エラー
@app.errorhandler(404)
def error404(error):
    return rt('errors/404.html')

@app.errorhandler(500)
def error500(error):
    return rt('errors/500.html'),500

if __name__ == '__main__':
    app.run(debug=True)