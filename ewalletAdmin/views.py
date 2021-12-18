import json
import datetime
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages
from django.core import serializers
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from ewallet.models import *
from ewallet.decorators import *
from .forms import *
from .filters import *
from .serializers import *


def registerPage(request):
    # create_superuser(username, email=None, password=None, **extra_fields)

    # form = CreateUserForm()
    # if request.method == 'POST':
    #     # create a form instance and populate it with data from the request:
    #     form = CreateUserForm(request.POST)
    #     # check whether it's valid:
    #     if form.is_valid():
    #         user = form.save()
    #         username = form.cleaned_data.get('username')

    #         group = Group.objects.get_or_create(name='parent')
    #         group.user_set.add(user)

    #         Parent.objects.create(
    #             user=user,
    #             name=user.username,
    #         )
    #         ParentWallet.objects.create(
    #             parent=user.parent,
    #         )

    #         messages.success(
    #             request, 'Your account was created succesfully, ' + username)
    # return redirect('/login/')

    context = {
        # 'form': form
    }
    return render(request, "ewallet/register.html", context)


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/admin2/')
        else:
            messages.info(request, 'Username OR password is incorrect')
    context = {}
    return render(request, "ewalletAdmin/login.html", context)


def logoutUser(request):
    logout(request)
    return redirect('/admin2/login/')


@login_required(login_url='/admin2/login/')
def homepage(request):
    transactions = Transaction.objects.all()[:5]
    students = Student.objects.all()
    parents = Parent.objects.all()

    context = {
        'transactions': transactions,
        'students': students,
        'parents': parents,
    }
    return render(request, "ewalletAdmin/home.html", context)

# -------------- Student Views --------------


class StudentCreateView(CreateView):
    model = Student
    fields = '__all__'
    template_name = 'ewalletAdmin/student_form.html'
    success_url = "/admin2/students/"


def StudentCreateView2(request):
    # parent = Parent.objects.get(id=pk)
    form = StudentForm()

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = StudentForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            form.save()          

            return redirect('/admin2/students/')
        else:
            print("form not valid")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = StudentForm()

    context = {
        'form': form,
    }
    return render(request, "ewalletAdmin/student_form.html", context)


class StudentListView(ListView):
    model = Student
    template_name = 'ewalletAdmin/student_list.html'
    paginate_by = 15
    # context_object_name = 'classgroup'

    # def get_queryset(self):
    #     return Student.objects.filter(classgroup='5 Sina')


class StudentDetailView(DetailView):
    model = Student
    fields = ('student_id', 'name', 'class_name', 'parent', 'card_id')
    template_name = 'ewalletAdmin/student_detail.html'


class StudentUpdateView(UpdateView):
    model = Student
    fields = ('student_id', 'name', 'class_name', 'parent', 'card_id')
    template_name = 'ewalletAdmin/student_form.html'
    success_url = "/admin2/students/"


class StudentDeleteView(DeleteView):
    model = Student
    fields = '__all__'
    template_name = 'ewalletAdmin/student_confirm_delete.html'
    success_url = "/admin2/students/"


# def manageStudent(request):
#     student = Student.objects.all()

#     myFilter = StudentFilter(request.GET, queryset=student)
#     student = myFilter.qs

#     context = {
#         'students': student,
#         'myFilter': myFilter,
#     }
#     return render(request, "ewalletAdmin/manage_student.html", context)


# def createStudent(request):

#     student_form = StudentForm()
#     if request.method == 'POST':
#         # create a form instance and populate it with data from the request:
#         student_form = StudentForm(request.POST)
#         # check whether it's valid:
#         if student_form.is_valid():
#             student_form.save()
#             return redirect('/admin2/students/')

#     # if a GET (or any other method) we'll create a blank form
#     else:
#         student_form = StudentForm()

#     context = {
#         'student_form': student_form,
#     }
#     return render(request, "ewalletAdmin/student_form.html", context)


# def updateStudent(request, pk):
#     student = Student.objects.get(student_id=pk)

#     student_form = StudentForm(instance=student)
#     if request.method == 'POST':
#         student_form = StudentForm(request.POST, instance=student)
#         if student_form.is_valid():
#             student_form.save()
#             return redirect('/admin2/students/')

#     context = {
#         'student_form': student_form,
#     }
#     return render(request, "ewalletAdmin/student_form.html", context)

# -------------- Parent Views --------------


class ParentCreateView(CreateView):
    model = Parent
    fields = '__all__'
    template_name = 'ewalletAdmin/parent_form.html'
    success_url = "/admin2/parents/"


class ParentListView(ListView):
    model = Parent
    template_name = 'ewalletAdmin/parent_list.html'
    paginate_by = 15
    # context_object_name = 'classgroup'

    # def get_queryset(self):
    #     return Student.objects.filter(classgroup='5 Sina')


# class ParentDetailView(DetailView):
#     model = Parent
#     template_name = 'ewalletAdmin/parent_detail.html'


def ParentDetailView2(request, pk):
    parent = Parent.objects.get(id=pk)
    student = parent.student_set.all()
    context = {
        'parent': parent,
        'student': student,
    }

    return render(request, "ewalletAdmin/parent_detail.html", context)


class ParentUpdateView(UpdateView):
    model = Parent
    fields = [
        'name',
        'phone',
        'email'
    ]
    template_name = 'ewalletAdmin/parent_form.html'
    success_url = "/admin2/parents/"


class ParentDeleteView(DeleteView):
    model = Parent
    fields = '__all__'
    template_name = 'ewalletAdmin/parent_confirm_delete.html'
    success_url = "/admin2/parents/"

# -------------- Product Views --------------


class ProductCreateView(CreateView):
    model = Product
    fields = '__all__'
    template_name = 'ewalletAdmin/product_form.html'
    success_url = "/admin2/products/"


class ProductListView(ListView):
    model = Product
    template_name = 'ewalletAdmin/product_list.html'
    paginate_by = 10
    # context_object_name = 'classgroup'

    # def get_queryset(self):
    #     return Student.objects.filter(classgroup='5 Sina')


class ProductDetailView(DetailView):
    model = Product
    template_name = 'ewalletAdmin/product_detail.html'


class ProductUpdateView(UpdateView):
    model = Product
    fields = '__all__'
    template_name = 'ewalletAdmin/product_form.html'
    success_url = "/admin2/products/"


class ProductDeleteView(DeleteView):
    model = Product
    fields = '__all__'
    template_name = 'ewalletAdmin/product_confirm_delete.html'
    success_url = "/admin2/products/"


# -------------- Store Views --------------
# To record payment at school


def storePage(request):
    products = Product.objects.all()

    myFilter = ProductFilter(request.GET, queryset=products)
    products = myFilter.qs

    if 'check' in request.GET:
        students = Student.objects.all()
        card = CardFilter(request.GET, queryset=students)
        students = card.qs
        count = 0
        for i in students:
            count += 1
            print(count)

    context = {
        'products': products,
        'myFilter': myFilter,
    }
    return render(request, "ewalletAdmin/store.html", context)

# -------------- Transaction  Views --------------


# class TransactionCreateView(CreateView):
#     model = Transaction
#     fields = [
#         'student',
#         'amount'
#     ]

#     template_name = 'ewalletAdmin/transaction_form.html'
#     success_url = "/admin2/transactions/"

def TransactionCreateView2(request):
    student = serializers.serialize("json", Student.objects.all())

    if request.method == 'POST':
        details = TransactionForm(request.POST)

        if details.is_valid():
            post = details.save(commit=False)
            post.save()
            return HttpResponse("data submitted successfully")

        else:
            return HttpResponse("data invalid")

    else:
        form = TransactionForm(None)

        context = {
            'form': form,
            'student': student,
        }
        return render(request, "ewalletAdmin/transaction_form.html", context)


def processTransaction(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    student = Student.objects.get(student_id=data['form']['student'])

    if(student.card_id == data['form']['card_id']):
        print(student.card_id, data['form']['card_id'])

        if (student.wallet_balance > float(data['form']['amount'])):
            student.wallet_balance -= float(data['form']['amount'])
            student.save()

            Transaction.objects.create(
                student=student,
                parent=student.parent,
                transaction_id=transaction_id,
                date=datetime.datetime.now(),
                transaction_type='Scan & Pay',
                description='Co-op',
                amount=data['form']['amount'],
            )
            return JsonResponse('Payment Complete', safe=False)

        else:
            return JsonResponse('Not enough balance', safe=False)

    else:
        print(student.card_id, data['form']['card_id'])
        return JsonResponse('Card not matched', safe=False)


class TransactionListView(ListView):
    model = Transaction
    template_name = 'ewalletAdmin/transaction_list.html'
    paginate_by = 10
    # context_object_name = 'classgroup'

    # def get_queryset(self):
    #     return Student.objects.filter(classgroup='5 Sina')


class TransactionDetailView(DetailView):
    model = Transaction
    template_name = 'ewalletAdmin/transaction_detail.html'


class TransactionUpdateView(UpdateView):
    model = Transaction
    fields = [
        'transaction_id',
        'transaction_type',
        'description',
        's_wallet',
        'amount'
    ]
    template_name = 'ewalletAdmin/transaction_form.html'
    success_url = "/admin2/transactions/"


class TransactionDeleteView(DeleteView):
    model = Transaction
    fields = [
        'transaction_id',
        'transaction_type',
        'description',
        's_wallet',
        'amount'
    ]
    template_name = 'ewalletAdmin/transaction_confirm_delete.html'
    success_url = "/admin2/transactions/"


# def transactions(request):
#     transactions = Transaction.objects.all()

#     myFilter = TransactionFilter(request.GET, queryset=transactions)
#     transactions = myFilter.qs

#     context = {
#         'transactions': transactions,
#         'myFilter': myFilter,
#     }
#     return render(request, "ewalletAdmin/transactions.html", context)

# -------------- Order Views --------------


class OrderListView(ListView):
    model = Order
    template_name = 'ewalletAdmin/order_list.html'
    paginate_by = 10


class OrderUpdateView(UpdateView):
    model = Order
    fields = ['received', ]
    template_name = 'ewalletAdmin/order_form.html'
    success_url = "/admin2/orders/"
