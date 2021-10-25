from django.forms import ModelForm
from django.forms.widgets import NumberInput, TextInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from ewallet.models import Student, ParentWallet, StudentWallet

class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        exclude = ('parent', 'card_id', 'batch')
        widgets = {            
            'name': TextInput(attrs={'size': 60}),
        }
        # labels = {
        #     'name': 'Writer',
        # }
        # help_texts = {
        #     'name': 'Some useful help text.',
        # }
        # error_messages = {
        #     'name': {
        #         'max_length': "This writer's name is too long.",
        #     },
        # }

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

class TransferForm(ModelForm):
    class Meta:
        model = ParentWallet
        fields = '__all__'
        