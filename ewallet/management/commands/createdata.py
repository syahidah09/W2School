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
    "Science PT3",
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

class Provider(faker.providers.BaseProvider):
        def store_category(self):
            return self.random_element(CATEGORIES)

        def store_product(self):
            return self.random_element(PRODUCT)

        def student_classname(self):
            return self.random_element(CLASS_NAME)

class Command(BaseCommand):
    help = "Command Information"

    def handle(self, *args, ** kwargs):
        fake = Faker()
        fake.add_provider(Provider)

        # Create users (parent)        
        for _ in range(5):
            first_name = fake.first_name()
            last_name = fake.last_name()
            username = first_name+last_name
            email = fake.email()            
            password = "qasdfghj"
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
            phone = "01"+str(random.randrange(1, 99999999, 8))            
            Parent.objects.create(user=user, phone=phone)
            group, created = Group.objects.get_or_create(name='parent')
            user.groups.add(group)

        check_parent = Parent.objects.all().count()
        self.stdout.write(self.style.SUCCESS(
            f"No of parents: {check_parent}"))

        # Create Students
        for _ in range(8):            
            student_id = fake.unique.random_int(min=100, max=199)            
            parent = random.choice(Parent.objects.all())            
            last_name = parent.user.first_name # parent's first name
            first_name = fake.first_name()             
            class_name = fake.student_classname()
            Student.objects.create(student_id=student_id, first_name=first_name, last_name=last_name, class_name=class_name, parent=parent)

        check_student = Student.objects.all().count()
        self.stdout.write(self.style.SUCCESS(
            f"No of students: {check_student}"))

        # Create Products
        for _ in range(15):
            name = fake.unique.store_product()
            category = fake.store_category()
            price = round(random.uniform(0.5, 5.5), 2)
            quantity = fake.random_int(min=0, max=10)  
            Product.objects.create(name=name, price=price, category=category, quantity=quantity)

        check_product = Product.objects.all().count()
        self.stdout.write(self.style.SUCCESS(
            f"No of products: {check_product}"))

        
