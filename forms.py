from flask_wtf import FlaskForm
from wtforms.fields import(StringField,IntegerField,DateField,SelectField,TextAreaField,SubmitField)
from wtforms.validators import(DataRequired,InputRequired,NumberRange,Optional,Length)
from validators import multiple_of_10, not_future

class RecordForm(FlaskForm):
    date = DateField('日付：', validators=[DataRequired('日付は必須項目です'),not_future],format="%Y-%m-%d",render_kw={"placeholder":"yyyy/mm/dd"})
    title = StringField('機種・レース：', validators=[Optional(),Length(max=100, message='100文字以内で入力してください')],render_kw={"placeholder":"(例)日本ダービー"})
    category_id = SelectField('カテゴリ：', coerce=int,validators=[DataRequired('カテゴリを選択してください')])
    place_id = SelectField('場所：', coerce=int,validators=[DataRequired('場所を選択してください')])
    investment = IntegerField('投資：', default=0,validators=[InputRequired('投資額を入力してください'),NumberRange(min=0,message='値は0以上にしてください'),multiple_of_10])
    payout = IntegerField('回収：', default=0,validators=[InputRequired('回収額を入力してください'),NumberRange(min=0,message='値は0以上にしてください'),multiple_of_10])
    memo = TextAreaField('メモ：', validators=[Optional(),Length(max=500, message='メモは500文字以内で入力してください')])
    submit = SubmitField('登録')
    
class PlaceForm(FlaskForm):
    name = StringField('店舗名・開催場名：', validators=[DataRequired('名前は必須項目です'),Length(max=50, message='50文字以内で入力してください')],render_kw={"placeholder":"(例)東京競馬場"})
    category_id = SelectField('カテゴリ：', coerce=int,validators=[DataRequired('カテゴリを選択してください')])
    submit = SubmitField('登録')
    
class CategoryForm(FlaskForm):
    name = StringField('カテゴリ名：', validators=[DataRequired('名前は必須項目です'),Length(max=50, message='50文字以内で入力してください')],render_kw={"placeholder":"(例)競馬"})
    submit = SubmitField('登録')