from flask import Flask, render_template as rt, request, redirect,url_for, flash
import services.record_service as rs
import services.place_service as ps
import services.category_service as cs
from models import Record, Place, Category
from datetime import datetime
from forms import RecordForm, PlaceForm, CategoryForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key-2026'

@app.route('/')
def index():
    return rt('index.html',total = rs.get_totalProfit(),win=rs.get_winRate())

@app.route('/records')
def show_records():
    return rt('records/list.html',records = rs.get_records())

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

@app.route('/places')
def place_master():
    return rt('places/list.html', places = ps.get_places())

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
        flash('この項目は削除できません', 'error')
    elif ps.has_records(id):
        flash('この場所は収支で使用されているため削除できません', 'error')
    else:
        ps.delete_place(id)
        flash('場所を削除しました', 'success')
    return redirect(url_for('place_master'))

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
        flash('この項目は削除できません', 'error')
    elif cs.has_records(id):
        flash('このカテゴリは収支で使用されているため削除できません', 'error')
    else:
        cs.delete_category(id)
        flash('カテゴリを削除しました', 'success')
    return redirect(url_for('category_master'))

if __name__ == '__main__':
    app.run(debug=True)