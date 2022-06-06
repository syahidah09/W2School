from django.db.models import fields
from django_filters import *

from .models import *

TRANSACTION_TYPES = [
    ('Deposit', 'Deposit'),
    ('Transfer', 'Transfer'),
    ('Payment', 'Payment'),
]

DESCRIPTION = [
    ('Canteen', 'Canteen'),
    ('Co-op', 'Co-op'),
    ('e-Store', 'e-Store'),
    ('School Fee', 'School Fee'),
]


class TransactionFilter(FilterSet):
    date = DateFromToRangeFilter(label='Date Range')
    transaction_type = ChoiceFilter(choices=TRANSACTION_TYPES)
    description = ChoiceFilter(choices=DESCRIPTION)

    class Meta:
        model = Transaction
        fields = ('date', 'transaction_type', 'description')


class StudenttFilter(FilterSet):
    class Meta:
        model = Student
        fields = ('student_id',)


CATEGORIES = [
    ("School Items", "School Items"),
    ("Stationery", "Stationery"),
    ("Workbook", "Workbook"),
    ("Food & Drinks", "Food & Drinks"),
]


class ProductFilter(FilterSet):
    name = CharFilter(lookup_expr='icontains', label='Name')
    category = ChoiceFilter(choices=CATEGORIES)

    class Meta:
        model = Product
        fields = ['name', 'category', ]
