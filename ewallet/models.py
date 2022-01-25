from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User


class Parent(models.Model):
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE)    
    phone = models.CharField(max_length=200, null=True, blank=True)    
    wallet_balance = models.FloatField(default=0)

    def get_absolute_url(self):
        return reverse('ewalletAdmin:parent-detail', args=[str(self.id)])

    def get_absolute_url2(self):
        return reverse('ewallet:parent-detail', args=[str(self.id)])

    def get_absolute_url3(self):
        return reverse('ewalletAdmin:student-create', args=[str(self.id)])

    def get_update(self):
        return reverse('ewalletAdmin:parent-update', args=[str(self.id)])

    def get_update2(self):
        return reverse('ewallet:parent-update', args=[str(self.id)])

    def confirm_delete(self):        
        return reverse('ewalletAdmin:parent-delete', args=[str(self.id)])

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"  


class Student(models.Model):
    CLASS_NAME = [
        ('1A', '1A'),
        ('1B', '1B'),
        ('2A', '2A'),
        ('2B', '2B'),
        ('3A', '3A'),
        ('3B', '3B'),
        ('4A', '4A'),
        ('4B', '4B'),
        ('5A', '5A'),
        ('5B', '5B'),
    ]

    student_id   = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    class_name   = models.CharField(
                 max_length=10, choices=CLASS_NAME, blank=True)
    parent       = models.ForeignKey(
                Parent, null=True, blank=True, on_delete=models.SET_NULL)
    card_id     = models.CharField(max_length=10, unique=True, null=True, blank=True,)
    wallet_balance = models.FloatField(default=0)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = u'%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    @property
    def get_total_spent(self):
        transaction = self.transaction_set.all()
        total = sum([item.amount for item in transaction])
        return "{:.2f}".format(total)

    def get_absolute_url(self):
        return reverse('ewalletAdmin:student-detail', args=[str(self.student_id)])
    


    def get_update(self):
        return reverse('ewalletAdmin:student-update', args=[str(self.student_id)])

    def confirm_delete(self):
        return reverse('ewalletAdmin:student-delete', args=[str(self.student_id)])    

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ['student_id']


class Product(models.Model):
    CATEGORIES = [
    ("School Items", "School Items"),
    ("Stationery", "Stationery"),
    ("Workbook", "Workbook"),
    ("Food & Drinks", "Food & Drinks"), 
    ]
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    category = models.CharField(max_length=200, blank=True, choices=CATEGORIES)
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
    date_ordered = models.DateTimeField(auto_now_add=False)
    complete = models.BooleanField(default=False)
    receive = models.BooleanField(default=False)

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
    date_added = models.DateTimeField(auto_now_add=False)

    def __str__(self):
        return str(self.product.name)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('Deposit', 'Deposit'),
        ('Transfer', 'Transfer'),
        ('Payment', 'Payment'),        
    ]

    DESCRIPTION = [        
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
    date            = models.DateTimeField(auto_now_add=False)
    amount          = models.FloatField(default=0)
    transaction_type = models.CharField(
                    max_length=15, choices=TRANSACTION_TYPES, default='Payment')
    description     = models.CharField(
                    max_length=15, blank=True, choices=DESCRIPTION, default="-")
    order           = models.ForeignKey(
                    Order, null=True, blank=True, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('ewalletAdmin:transaction-detail', args=[str(self.id)])

    def get_update(self):
        return reverse('ewalletAdmin:transaction-update', args=[str(self.id)])

    def confirm_delete(self):
        return reverse('ewalletAdmin:transaction-delete', args=[str(self.id)])

    def get_absolute_url2(self):
        return reverse('ewallet:transaction-detail', args=[str(self.id)])

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ['-date']  # - means desceding

class Notifcation(models.Model):
    parent      = models.ForeignKey(
                Parent, null=True, blank=True, on_delete=models.SET_NULL)
    subject     = models.CharField(max_length=200, null=True)
    content     = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.subject
        