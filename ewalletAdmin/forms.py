from django.forms import ModelForm
from ewallet.models import Student
from .models import Product

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
        