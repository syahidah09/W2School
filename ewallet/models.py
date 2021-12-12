from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User


class Parent(models.Model):
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    wallet_balance = models.FloatField(default=0)

    def get_absolute_url(self):
        return reverse('ewalletAdmin:parent-detail', args=[str(self.id)])

    def get_absolute_url2(self):
        return reverse('ewallet:parent-detail', args=[str(self.id)])

    def get_update(self):
        return reverse('ewalletAdmin:parent-update', args=[str(self.id)])

    def get_update2(self):
        return reverse('ewallet:parent-update', args=[str(self.id)])

    def confirm_delete(self):
        return reverse('ewalletAdmin:parent-delete', args=[str(self.id)])

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Student(models.Model):
    CLASS_NAME = [
        ('1A', '1A'),
        ('1B', '1B'),
        ('2A', '2A'),
        ('2B', '2B'),
    ]

    student_id   = models.IntegerField(primary_key=True)
    name         = models.CharField(max_length=200, null=True)
    class_name   = models.CharField(
                 max_length=10, choices=CLASS_NAME, default='1A')
    parent       = models.ForeignKey(
                Parent, null=True, blank=True, on_delete=models.SET_NULL)
    card_id     = models.CharField(max_length=10, unique=True)
    wallet_balance = models.FloatField(default=0)

    def get_absolute_url(self):
        return reverse('ewalletAdmin:student-detail', args=[str(self.student_id)])

    def get_update(self):
        return reverse('ewalletAdmin:student-update', args=[str(self.student_id)])

    def confirm_delete(self):
        return reverse('ewalletAdmin:student-delete', args=[str(self.student_id)])

    def __str__(self):
        return f"{self.student_id} {self.name}"

    class Meta:
        ordering = ['student_id']


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


class Order(models.Model):
    parent   = models.ForeignKey(
            Parent, null=True, blank=True, on_delete=models.SET_NULL)
    student = models.ForeignKey(
            Student, null=True, blank=True, on_delete=models.SET_NULL)  # as receiver for parent's on9 purchase
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(
            default=False, null=True, blank=False)  # complete
    received = models.BooleanField(default=False, null=True, blank=False)

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

    def get_update(self):
        return reverse('ewalletAdmin:order-update', args=[str(self.id)])


class OrderItem(models.Model):
    product = models.ForeignKey(
            Product, null=True, blank=True, on_delete=models.SET_NULL)
    order   = models.ForeignKey(
            Order, null=True, blank=True, on_delete=models.SET_NULL)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


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
    transaction_id  = models.CharField(max_length=100, null=True)
    parent          = models.ForeignKey(
                    Parent, null=True, blank=True, on_delete=models.SET_NULL)
    student         = models.ForeignKey(
                    Student, null=True, blank=True, on_delete=models.SET_NULL)  # as receiver for parent's on9 purchase   
    date            = models.DateTimeField(auto_now_add=True)
    amount          = models.FloatField(default=0)
    transaction_type = models.CharField(
                    max_length=15, choices=TRANSACTION_TYPES, default='Payment')
    description     = models.CharField(
                    max_length=15, choices=DESCRIPTION, default='Online')
    order           = models.OneToOneField(
                    Order, null=True, blank=True, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('ewalletAdmin:transaction-detail', args=[str(self.id)])

    def get_update(self):
        return reverse('ewalletAdmin:transaction-update', args=[str(self.id)])

    def confirm_delete(self):
        return reverse('ewalletAdmin:transaction-delete', args=[str(self.id)])

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ['-date']  # - means desceding


