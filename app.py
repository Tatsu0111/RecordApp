from flask import Flask, render_template as rt, request, redirect,url_for
import services.record_service as rs
import services.place_service as ps
import services.category_service as cs
from models import Record, Place, Category
from datetime import datetime
# from forms import RecordForm

app = Flask(__name__)

@app.route('/')
def index():
    return rt('index.html',total = rs.get_totalProfit(),win=rs.get_winRate())

@app.route('/records')
def show_records():
    return rt('records/list.html',records = rs.get_records())

@app.route('/records/add', methods=['GET','POST'])
@app.route('/records/<int:id>/edit', methods=['GET','POST'])
def record_form(id=None):
    if request.method == 'POST':
        while True:
            try:
                date = datetime.strptime(request.form["date"], "%Y-%m-%d").date()
                break
            except ValueError:
                error = '正しく入力してください'
                return rt('records/form.html', row=None, categories=cs.get_categories(), places=ps.get_places(), error=error)
        title = request.form["title"]
        category_id = int(request.form["category_id"])
        place_id = int(request.form["place_id"])
        investment = int(request.form["investment"])
        payout = int(request.form["payout"])
        memo = request.form["memo"]
        if id is None:
            record = Record(
                date = date,
                title = title,
                category_id = category_id,
                place_id = place_id,
                investment = investment,
                payout = payout,
                memo = memo
            )
            rs.insert_record(record)
        else:
            rs.update_record(
                id,
                data = {
                'date':date,
                'title':title,
                'category_id':category_id,
                'place_id':place_id,
                'investment':investment,
                'payout':payout,
                'memo':memo
                }            
            )
        return redirect(url_for('show_records'))
    if id is None:
        row = None
    else:
        row = rs.get_record(id)
    return rt('records/form.html',row=row,categories=cs.get_categories(),places=ps.get_places())

@app.route('/records/<int:id>/delete',methods=['POST'])
def record_delete(id):
    rs.delete_record(id)
    return redirect(url_for('show_records'))

@app.route('/places')
def place_master():
    return rt('places/list.html', places = ps.get_places())

@app.route('/places/add', methods=['GET','POST'])
@app.route('/places/<int:id>/edit', methods=['GET','POST'])
def place_form(id=None):
    if request.method == 'POST':
        name = request.form["name"]
        category_id = int(request.form["category_id"])
        if id is None:
            place = Place(
                name = name,
                category_id = category_id,
            )
            ps.insert_place(place)
        else:
            ps.update_place(
                id,
                data = {
                'name':name,
                'category_id':category_id
                }            
            )
        return redirect(url_for('place_master'))
    if id is None:
        row = None
    else:
        row = ps.get_place(id)
    return rt('places/form.html',row=row,categories=cs.get_categories())

@app.route('/places/<int:id>/delete',methods=['POST'])
def place_delete(id):
    ps.delete_place(id)
    return redirect(url_for('place_master'))

@app.route('/categories')
def category_master():
    return rt('categories/list.html', categories = cs.get_categories())

@app.route('/categories/add', methods=['GET','POST'])
@app.route('/categories/<int:id>/edit', methods=['GET','POST'])
def category_form(id=None):
    if request.method == 'POST':
        name = request.form["name"]
        if id is None:
            category = Category(
                name = name
            )
            cs.insert_category(category)
        else:
            cs.update_category(
                id,
                data = {
                'name':name
                }            
            )
        return redirect(url_for('category_master'))
    if id is None:
        row = None
    else:
        row = cs.get_category(id)
    return rt('categories/form.html',row=row)

@app.route('/categories/<int:id>/delete',methods=['POST'])
def category_delete(id):
    cs.delete_category(id)
    return redirect(url_for('category_master'))

if __name__ == '__main__':
    app.run(debug=True)