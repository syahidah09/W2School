from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User


class Parent(models.Model):
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse('ewalletAdmin:parent-detail', args=[str(self.id)])

    def get_update(self):
        return reverse('ewalletAdmin:parent-update', args=[str(self.id)])

    def confirm_delete(self):
        return reverse('ewalletAdmin:parent-delete', args=[str(self.id)])

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']



class Student(models.Model):
    student_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200, null=True)
    classgroup = models.CharField(max_length=10)
    batch = models.CharField(max_length=5)
    card_id = models.IntegerField()
    parent = models.ForeignKey(
        Parent,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )   

    def get_absolute_url(self):
        return reverse('ewalletAdmin:student-detail', args=[str(self.student_id)])

    def get_update(self):
        return reverse('ewalletAdmin:student-update', args=[str(self.student_id)])

    def confirm_delete(self):
        return reverse('ewalletAdmin:student-delete', args=[str(self.student_id)])

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['student_id']


class ParentWallet(models.Model):
    parent = models.OneToOneField(
        Parent, null=True, blank=True, on_delete=models.CASCADE)
    balance = models.FloatField(default=0)

    def __str__(self):
        return self.parent.name


class StudentWallet(models.Model):
    student = models.OneToOneField(
        Student, null=True, blank=True, on_delete=models.CASCADE)
    balance = models.FloatField(default=0)
    parent = models.ForeignKey(
        Parent, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.student.name


class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    quantity = models.IntegerField(default=0, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse('ewalletAdmin:product-detail', args=[str(self.id)])

    def get_update(self):
        return reverse('ewalletAdmin:product-update', args=[str(self.id)])

    def confirm_delete(self):
        return reverse('ewalletAdmin:product-delete', args=[str(self.id)])

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = '/static/img/placeholder.png'
        return url
    
    class Meta:
        ordering = ['name']


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('Deposit', 'Deposit'),
        ('Transfer', 'Transfer'),
        ('Payment', 'Payment'),
        ('Scan & Pay', 'Scan & Pay'),
    ]

    DESCRIPTION = [
        ('Online', 'Online'),
        ('Reload', 'Reload'),
        ('Canteen', 'Canteen'),
        ('Co-op', 'Co-op'),
        ('e-Store', 'e-Store'),
        ('School Fee', 'School Fee'),
    ]
    transaction_id = models.CharField(max_length=100, null=True)
    parent = models.ForeignKey(
        Parent, null=True, blank=True, on_delete=models.SET_NULL)    
    s_wallet = models.ForeignKey(
        StudentWallet, null=True, blank=True, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField(default=0)    
    transaction_type = models.CharField(
        max_length=15, choices=TRANSACTION_TYPES, default='Payment')
    description = models.CharField(
        max_length=15, choices=DESCRIPTION, default='Online')

    def get_absolute_url(self):
        return reverse('ewalletAdmin:transaction-detail', args=[str(self.id)])

    def get_update(self):
        return reverse('ewalletAdmin:transaction-update', args=[str(self.id)])

    def confirm_delete(self):
        return reverse('ewalletAdmin:transaction-delete', args=[str(self.id)])

    def __str__(self):
        return str(self.id)

    @property
    def add(self):
        sum = self.parent.parentwallet.balance + self.amount
        return sum

    @property
    def subtract(self):        
        sum = self.parent.parentwallet.balance - self.amount
        return sum


class Order(models.Model):
    parent = models.ForeignKey(
        Parent, null=True, blank=True, on_delete=models.SET_NULL)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(
        Product, null=True, blank=True, on_delete=models.SET_NULL)
    order = models.ForeignKey(
        Order, null=True, blank=True, on_delete=models.SET_NULL)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    parent = models.ForeignKey(
        Parent, null=True, blank=True, on_delete=models.SET_NULL)
    order = models.ForeignKey(
        Order, null=True, blank=True, on_delete=models.SET_NULL)
    address = models.CharField(max_length=100, null=False)
    city = models.CharField(max_length=100, null=False)
    state = models.CharField(max_length=100, null=False)
    zipcode = models.CharField(max_length=100, null=False)
    date_added = models.DateTimeField(auto_now_add=True)
