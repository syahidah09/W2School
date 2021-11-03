from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client
from django.contrib.auth.mixins import LoginRequiredMixin

from ewallet.models import ParentWallet, StudentWallet, Student, Parent, Transaction

class EwalletViewsTestCase(TestCase):
    def setUp(self):
        # Create two users
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')

        test_user1.save()
        test_user2.save()

        parent = Parent.objects.create(
            user=test_user1,
            name='Abu'
        )
        # Create 30 BookInstance objects
        number_of_students = 10
        for i in range(number_of_students):
            classgroup='5Sina'
            batch='21001'
            Student.objects.create(
                student_id=i,
                name='Zack'+str(i),
                classgroup=classgroup,
                batch=batch,
                card_id=i,
                parent=parent,
            )

    def test_register(self):
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_redirect_if_not_logged_in(self):
        # if user.groups.filter(name="parent"):
        # print("User " + user.username + " is in a group parent")
        response = self.client.get('/home/')
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))
    
    def test_logout(self):
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 302)

    # def test_homepage(self):
    #     login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
    #     # response = self.client.get('/home/') AttributeError: 'User' object has no attribute 'parent'

    #     self.assertRedirects(response, '/accounts/login/?next=/ewallet/home/')
    #     # Check our user is logged in
    #     self.assertEqual(str(response.context['user']), 'testuser1')
    #     # self.assertEqual(response.status_code, 200)
    #     self.assertRedirects(response, '/login/')
    #     # Check we used correct template
    #     self.assertTemplateUsed(response, 'ewallet/login2.html')
    
    # def test_walletpage(self):
    #     resp = self.client.get('/wallet/')
    #     self.assertEqual(resp.status_code, 200)

    def test_transaction_history(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        resp = self.client.get('/transaction_history/')

        # Check our user is logged in
        self.assertEqual(str(resp.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(resp.status_code, 200)
        # Check we used correct template
        self.assertTemplateUsed(resp, 'ewallet/transaction_history.html')

    def test_store(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        resp = self.client.get('/store/')

        self.assertEqual(str(resp.context['user']), 'testuser1')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'ewallet/store.html')
    
    
        