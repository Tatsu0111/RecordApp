from wtforms import Form
from wtforms.fields import(StringField,IntegerField,DateField,SelectField,TextAreaField,SubmitField)
from wtforms.validators import(DataRequired,NumberRange,Optional)

class RecordForm(Form):
    date = DateField('日付：', validators=[DataRequired('日付は必須項目です')],format="%Y-%m-%d",render_kw={"placeholder":"yyyy/mm/dd"})
    # title = StringField('機種・レース：', validators=[Optional()],render_kw={"placeholder":"(例)日本ダービー"})
    # category_id = 
    # place_id = 
    # investment = IntegerField('投資：', validators=[])
    # payout = 
    # memo = 
    # created_at = 
    # update_at = 