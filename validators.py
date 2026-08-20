from wtforms.validators import ValidationError
from datetime import date
from wtforms.validators import ValidationError
import services.place_service as ps, services.category_service as cs

def not_future(form, field):
    if field.data is not None and field.data > date.today():
        raise ValidationError('未来の日付は指定できません')
    
def multiple_of_10(form, field):
    if field.data is not None and field.data % 10 != 0:
        raise ValidationError('10円単位で入力してください')
    
def unique_place_name(form, field):
    if ps.get_place_by_name(field.data):
        raise ValidationError('この場所はすでに登録されています')
    
def unique_category_name(form, field):
    if cs.get_category_by_name(field.data):
        raise ValidationError('このカテゴリはすでに登録されています')