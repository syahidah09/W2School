from django.contrib import admin

from .models import Student, Parent, ParentWallet, StudentWallet, Transaction

# Register your models here.
# admin.site.register(Student)
@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')    
    search_fields = ('name','email')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'name')    
    search_fields = ('student_id','name')

@admin.register(ParentWallet)
class ParentWalletAdmin(admin.ModelAdmin):
    list_display = ('parent', 'balance')    
    search_fields = ('parent','balance')

@admin.register(StudentWallet)
class StudentWalletAdmin(admin.ModelAdmin):
    list_display = ('student', 'parent')    
    search_fields = ('student','parent')

# admin.site.register(ParentWallet)
# admin.site.register(StudentWallet)
admin.site.register(Transaction)



