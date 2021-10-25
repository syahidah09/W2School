from django.db import models
from django.contrib.auth.models import User


class Parent(models.Model):
    user = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL)
    # parent_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return self.name


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

    def __str__(self):
        return self.name


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
        Parent,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return self.student.name


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('Deposit', 'Deposit'),
        ('Payment', 'Payment'),
        ('Scan & Pay', 'Scan & Pay'),
    ]

    DESCRIPTION = [
        ('Canteen', 'Canteen'),
        ('Co-op', 'Co-op'),
        ('e-Store', 'e-Store'),
        ('School Fee', 'School Fee'),
    ]

    transaction_id = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField(default=0)
    transaction_type = models.CharField(
        max_length=15,
        choices=TRANSACTION_TYPES,
        default='Payment',
    )
    description = models.CharField(
        max_length=15,
        choices=DESCRIPTION,
        default='Canteen',
    )
