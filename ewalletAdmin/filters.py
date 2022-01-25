from django.db.models import fields
from django_filters import *
from .models import *
from ewallet.models import *
from django.contrib.auth.models import User

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


CLASS_NAME = [
    ('1A', '1A'),
    ('1B', '1B'),
    ('2A', '2A'),
    ('2B', '2B'),
    ('3A', '3A'),
    ('3B', '3B'),
    ('4A', '4A'),
    ('4B', '4B'),
    ('5A', '5A'),
    ('5B', '5B'),
]


class StudentFilter(FilterSet):
    student_id = NumberFilter()
    first_name = CharFilter(lookup_expr='icontains',label='First Name')
    last_name = CharFilter(lookup_expr='icontains',label='Last Name')
    class_name = ChoiceFilter(choices=CLASS_NAME)

    class Meta:
        model = Student
        fields = ['class_name', 'first_name', 'last_name', 'student_id']

class UserFilter(FilterSet):    
    first_name = CharFilter(lookup_expr='icontains',label='First Name')
    last_name = CharFilter(lookup_expr='icontains',label='Last Name')    

    class Meta:
        model = User
        fields = ['first_name', 'last_name',]

CATEGORIES = [
    ("School Items", "School Items"),
    ("Stationery", "Stationery"),
    ("Workbook", "Workbook"),
    ("Food & Drinks", "Food & Drinks"),
]


class ProductFilter(FilterSet):
    name = CharFilter(lookup_expr='icontains', label='Name')
    category = ChoiceFilter(choices=CATEGORIES)    
    price = NumberFilter()
    price__gt = NumberFilter(field_name='price', lookup_expr='gt')
    price__lt = NumberFilter(field_name='price', lookup_expr='lt')
    quantity = NumberFilter(field_name='quantity')
    quantity__gt = NumberFilter(field_name='quantity', lookup_expr='gt')
    quantity__lt = NumberFilter(field_name='quantity', lookup_expr='lt')    

    class Meta:
        model = Product
        fields = ['name', 'category', 'price', 'quantity']

class CardFilter(FilterSet):
     class Meta:
        model = Student
        fields = ['card_id',]

class OrderFilter(FilterSet):    
    # receive = BooleanFilter()
    date_ordered = DateFromToRangeFilter(label='Date Range')    

    class Meta:
        model = User
        fields = ['date_ordered',]