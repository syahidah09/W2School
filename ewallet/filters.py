from django.db.models import fields
import django_filters 
from django_filters import DateFilter

from .models import *

class TransactionFilter(django_filters.FilterSet):
    # start_date = DateFilter(field_name="timestamp", lookup_expr='gte')
    # end_date = DateFilter(field_name="timestamp", lookup_expr='lte')
    class Meta:
        model = Transaction
        fields = ('transaction_type', 'description' )

class StudenttFilter(django_filters.FilterSet):   
    class Meta:
        model = Student
        fields = ('student_id',)