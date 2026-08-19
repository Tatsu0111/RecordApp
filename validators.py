from wtforms.validators import ValidationError
from datetime import date
from wtforms.validators import ValidationError

def not_future(form, field):
    if field.data is not None and field.data > date.today():
        raise ValidationError('未来の日付は指定できません')
    
def multiple_of_10(form, field):
    if field.data is not None and field.data % 10 != 0:
        raise ValidationError('10円単位で入力してください')