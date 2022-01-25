# py manage.py createdata
from django.core.management.base import BaseCommand
from faker import Faker
import faker.providers
import random
from ewallet.models import *
from django.contrib.auth.models import User, Group

CATEGORIES = [
    "School Items",
    "Stationery",
    "Workbook",
    "Food & Drinks"
]

PRODUCT = [
    "Sport T-shirt",
    "School T-shirt",
    "Graph Book",
    "Test Pad",
    "Highlighter",
    "Ruler",
    "Stapler",
    "Pen",
    "Correction Tape",
    "Maths PT3",
    "Addmath SPM",
    "Science PT3",
    "Science SPM",
    "Snickers",
    "Mars",
    "Kit Kat",
    "Mentos",
    "Choki",
    "Oat Crunch",
    "Milo",
    "Nestum"
]

CLASS_NAME = [
    '1A',
    '1B',
    '2A',
    '2B',
    '3A',
    '3B',
    '4A',
    '4B',
    '5A',
    '5B',
]

TRANSACTION_TYPES = [
    # 'Deposit',
    # 'Transfer',
    'Payment',
]

DESCRIPTION = [
    'Canteen',
    'Co-op',
    'e-Store',
]


class Provider(faker.providers.BaseProvider):
    def store_category(self):
        return self.random_element(CATEGORIES)

    def store_product(self):
        return self.random_element(PRODUCT)

    def student_classname(self):
        return self.random_element(CLASS_NAME)

    def transaction_type(self):
        return self.random_element(TRANSACTION_TYPES)

    def description(self):
        return self.random_element(DESCRIPTION)


class Command(BaseCommand):
    help = "Command Information"

    def handle(self, *args, ** kwargs):
        fake = Faker()
        fake.add_provider(Provider)

        first_name = "Barry"
        last_name = "Allen"
        username = first_name+last_name
        email = first_name+str(fake.random_int(min=1, max=99))+"@example.com"
        password = "qasdfghj"
        user = User.objects.create_user(
            username=username, first_name=first_name, last_name=last_name, email=email, password=password)
        phone = "01"+str(random.randrange(1, 99999999, 8))
        Parent.objects.create(user=user, phone=phone)
        group, created = Group.objects.get_or_create(name='parent')
        user.groups.add(group)
        # Create users (parent)
        for _ in range(5):
            first_name = fake.first_name_male()
            last_name = fake.last_name_male()
            username = first_name+last_name
            email = first_name + \
                str(fake.random_int(min=1, max=99))+"@example.com"
            password = "qasdfghj"
            user = User.objects.create_user(
                username=username, first_name=first_name, last_name=last_name, email=email, password=password)
            phone = "01"+str(random.randrange(1, 99999999, 8))
            Parent.objects.create(user=user, phone=phone)
            group, created = Group.objects.get_or_create(name='parent')
            user.groups.add(group)

        check_parent = Parent.objects.all().count()
        self.stdout.write(self.style.SUCCESS(
            f"No of parents: {check_parent}"))

        # Create Students
        for _ in range(10):
            student_id = fake.unique.random_int(min=100, max=999)
            parent = random.choice(Parent.objects.all())
            last_name = parent.user.last_name  # parent's first name
            first_name = fake.first_name()
            class_name = fake.student_classname()
            Student.objects.create(student_id=student_id, first_name=first_name,
                                   last_name=last_name, class_name=class_name, parent=parent)

        check_student = Student.objects.all().count()
        self.stdout.write(self.style.SUCCESS(
            f"No of students: {check_student}"))

        # Create Products
        for _ in range(20):
            name = fake.unique.store_product()
            category = fake.store_category()
            price = round(random.uniform(0.5, 5.5), 1)
            quantity = fake.random_int(min=0, max=20)
            Product.objects.create(
                name=name, price=price, category=category, quantity=quantity)

        check_product = Product.objects.all().count()
        self.stdout.write(self.style.SUCCESS(
            f"No of products: {check_product}"))

        # Create Order
        for _ in range(15):
            parent = random.choice(Parent.objects.all())
            print("#1",parent.student_set.all())     
            while parent.student_set.all().exists() == False:
                parent = random.choice(Parent.objects.all())                
                print("#2",parent.student_set.all())            
            student = random.choice(parent.student_set.all())
            date_ordered = fake.past_date()
            complete = False
            Order.objects.create(
                parent=parent, student=student,
                date_ordered=date_ordered, complete=complete, )

        check = Order.objects.all().count()
        self.stdout.write(self.style.SUCCESS(
            f"No of order: {check}"))

        # Create Orderitem
        for _ in range(40):
            product = random.choice(Product.objects.all())
            order = random.choice(Order.objects.all())
            if order.orderitem_set.all().count() > 2:
                order = random.choice(Order.objects.all())
            quantity = fake.random_int(min=1, max=10)
            OrderItem.objects.create(
                product=product, order=order, quantity=quantity,)

        check = OrderItem.objects.all().count()
        self.stdout.write(self.style.SUCCESS(
            f"No of orderitem: {check}"))

        # Create Transactions
        for _ in range(15):
            transaction_id = fake.unique.random_int(min=10000, max=99999)
            parent = random.choice(Parent.objects.all())
            while parent.student_set.all().exists() == False:
                parent = random.choice(Parent.objects.all())
            student = random.choice(parent.student_set.all())
            date = fake.past_date()            
            transaction_type = fake.transaction_type()
            description = fake.description()
            order = random.choice(
                Order.objects.filter(complete = False))            
            order.complete = True
            order.save()            
            amount = order.get_cart_total
            Transaction.objects.create(
                transaction_id=transaction_id, order=order, parent=parent, student=student,
                date=date, amount=amount, transaction_type=transaction_type, description=description,)

        check = Transaction.objects.all().count()
        self.stdout.write(self.style.SUCCESS(
            f"No of transactions: {check}"))
