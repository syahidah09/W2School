from django.test import TestCase

from django.contrib.auth.models import User

from ewallet.models import ParentWallet, StudentWallet, Student, Parent, Transaction

# class YourTestClass(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         print("setUpTestData: Run once to set up non-modified data for all class methods.")
#         pass

#     def setUp(self):
#         print("setUp: Run once for every test method to setup clean data.")
#         pass

#     def test_false_is_false(self):
#         print("Method: test_false_is_false.")
#         self.assertFalse(False)

#     def test_false_is_true(self):
#         print("Method: test_false_is_true.")
#         self.assertTrue(True)

#     def test_one_plus_one_equals_two(self):
#         print("Method: test_one_plus_one_equals_two.")
#         self.assertEqual(1 + 1, 2)


class ParentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='Abu')
        Parent.objects.create(user=user, name=user.username)

    def test_name_label(self):
        # Get an parent object to test
        parent = Parent.objects.get(id=1)
        # Get the metadata for the required field and use it to query the required field data
        field_label = parent._meta.get_field('name').verbose_name
        # Compare the value to the expected result
        self.assertEqual(field_label, 'name')


class StudentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='Abu')
        parent = Parent.objects.create(user=user, name=user.username)
        Student.objects.create(student_id='1', name='Aliiii',
                               classgroup='5 Sina', batch='2021', card_id='21001', parent=parent)

    def test_name_label(self):
        student = Student.objects.get(student_id=1)
        field_label = student._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_string_representation(self):
        student = Student.objects.get(student_id=1)        
        self.assertEqual(str(student), student.name)

    def test_card_id_label(self):
        student = Student.objects.get(student_id=1)
        field_label = student._meta.get_field('card_id').verbose_name
        self.assertEqual(field_label, 'card id')
