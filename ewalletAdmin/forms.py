from django.forms import ModelForm
from ewallet.models import *

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        help_texts = {
            # 'name': "The product's name",
        }
        error_messages = {
            'name': {
                'max_length': "This writer's name is too long.",
            },
        }

class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ('student', 'amount',) 
