from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(OrderItem)
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'parent', 'complete')
    # search_fields = ('name', 'email')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity')

@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    search_fields = ('name', 'email')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'name')
    search_fields = ('student_id', 'name')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'transaction_type', 'parent', 'amount')
