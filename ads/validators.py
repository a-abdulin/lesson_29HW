from datetime import datetime

from rest_framework.exceptions import ValidationError
from dateutil.relativedelta import relativedelta

def create_not_true(value):
    if value:
        raise ValidationError('is_published must not be True in the begining')


def check_birth_date(value):
    age = relativedelta(datetime.today(), value).years

    if int(age) < 9:
        raise ValidationError(f"Возраст {age} лет не подходит!")

