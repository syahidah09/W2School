from django.contrib import admin

from .models import (
    Student,
    Parent,
    ParentWallet,
    StudentWallet,
    Transaction,
    Product,
    Order,
    OrderItem,
    ShippingAddress,
)

# Register your models here.
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'parent', 'complete', 'transaction_id')
    # search_fields = ('name', 'email')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'quantity')

@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    search_fields = ('name', 'email')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'name')
    search_fields = ('student_id', 'name')


@admin.register(ParentWallet)
class ParentWalletAdmin(admin.ModelAdmin):
    list_display = ('parent', 'balance')
    search_fields = ('parent', 'balance')


@admin.register(StudentWallet)
class StudentWalletAdmin(admin.ModelAdmin):
    list_display = ('student', 'parent')
    search_fields = ('student', 'parent')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'transaction_type', 'parent', 'amount')
