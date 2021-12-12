from django.db.models import fields
import django_filters 
from django_filters import DateFilter, NumberFilter

from .models import *
from ewallet.models import *

class TransactionFilter(django_filters.FilterSet):
    # start_date = DateFilter(field_name="timestamp", lookup_expr='gte')
    # end_date = DateFilter(field_name="timestamp", lookup_expr='lte')
    class Meta:
        model = Transaction
        fields = ('transaction_type', 'description' )

class StudentFilter(django_filters.FilterSet):    
    class Meta:
        model = Student
        fields = ('class_name', 'student_id')

class ProductFilter(django_filters.FilterSet):
    # less = NumberFilter(field_name="quantity", lookup_expr='lte')    
    class Meta:
        model = Product
        fields = ('name', 'quantity')

class CardFilter(django_filters.FilterSet):
    class Meta:
        model = Student
        fields = ('card_id',)    