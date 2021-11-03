from django.forms import ModelForm
from django.forms.widgets import NumberInput, TextInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from ewallet.models import Student, ParentWallet, StudentWallet, Transaction, Parent

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
        # this function will be used for the validation
    def clean(self):
 
        # data from the form is fetched using super function
        super(StudentForm, self).clean()
         
        # extract the username and text field from the data
        name = self.cleaned_data.get('name')
        
 
        # conditions to be met for the username length
        if len(name) < 5:
            self._errors['name'] = self.error_class([
                'Minimum 5 characters required'])        
 
        # return any errors if found
        return self.cleaned_data

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

class TransferForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ('amount',)
    
    def clean(self):
 
        # data from the form is fetched using super function
        super(TransferForm, self).clean()
         
        # extract the username and text field from the data
        amount = self.cleaned_data.get('amount')        
 
        # conditions to be met for the username length
        if float(amount) == 0:
            self._errors['amount'] = self.error_class([
                'Minimum RM 1 required'])      
        
        # return any errors if found
        return self.cleaned_data
    
class ReloadForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ('s_wallet', 'amount',)
    
    def clean(self):
 
        # data from the form is fetched using super function
        super(TransferForm, self).clean()
         
        # extract the username and text field from the data
        amount = self.cleaned_data.get('amount')        
 
        # conditions to be met for the username length
        if float(amount) == 0:
            self._errors['amount'] = self.error_class([
                'Minimum RM 1 required'])      
        
        # return any errors if found
        return self.cleaned_data
        