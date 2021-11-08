import json
import datetime
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView


from ewallet.models import *
from ewallet.decorators import allowed_users
from .forms import ProductForm, StudentForm
from .filters import TransactionFilter, StudentFilter, ProductFilter


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


# @unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/home/')
        else:
            messages.info(request, 'Username OR password is incorrect')
    context = {}
    return render(request, "ewallet/login.html", context)

# @allowed_users(allowed_roles=['admin'])


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

# Student Model Views


class StudentCreateView(CreateView):
    model = Student
    fields = '__all__'
    template_name = 'ewalletAdmin/student_form.html'
    success_url = "/admin2/students/"


class StudentListView(ListView):
    model = Student
    template_name = 'ewalletAdmin/student_list.html'
    paginate_by = 5
    # context_object_name = 'classgroup'

    # def get_queryset(self):
    #     return Student.objects.filter(classgroup='5 Sina')


class StudentDetailView(DetailView):
    model = Student
    template_name = 'ewalletAdmin/student_detail.html'


class StudentUpdateView(UpdateView):
    model = Student
    fields = '__all__'
    template_name = 'ewalletAdmin/student_form.html'
    success_url = "/admin2/students/"


class StudentDeleteView(DeleteView):
    model = Student
    fields = '__all__'
    template_name = 'ewalletAdmin/student_confirm_delete.html'
    success_url = "/admin2/students/"


def manageStudent(request):
    student = Student.objects.all()

    myFilter = StudentFilter(request.GET, queryset=student)
    student = myFilter.qs

    context = {
        'students': student,
        'myFilter': myFilter,
    }
    return render(request, "ewalletAdmin/manage_student.html", context)


def createStudent(request):

    student_form = StudentForm()
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        student_form = StudentForm(request.POST)
        # check whether it's valid:
        if student_form.is_valid():
            student_form.save()
            return redirect('/admin2/students/')

    # if a GET (or any other method) we'll create a blank form
    else:
        student_form = StudentForm()

    context = {
        'student_form': student_form,
    }
    return render(request, "ewalletAdmin/student_form.html", context)


def updateStudent(request, pk):
    student = Student.objects.get(student_id=pk)

    student_form = StudentForm(instance=student)
    if request.method == 'POST':
        student_form = StudentForm(request.POST, instance=student)
        if student_form.is_valid():
            student_form.save()
            return redirect('/admin2/students/')

    context = {
        'student_form': student_form,
    }
    return render(request, "ewalletAdmin/student_form.html", context)

# Parent Model Views
# class ParentCreateView(CreateView):
#     model = Parent
#     fields = '__all__'
#     template_name = 'ewalletAdmin/parent_form.html'
#     success_url ="/admin2/parents/"


class ParentListView(ListView):
    model = Parent
    template_name = 'ewalletAdmin/parent_list.html'
    paginate_by = 5
    # context_object_name = 'classgroup'

    # def get_queryset(self):
    #     return Student.objects.filter(classgroup='5 Sina')


class ParentDetailView(DetailView):
    model = Parent
    template_name = 'ewalletAdmin/parent_detail.html'


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

# Product Model Views


def productPage(request):
    products = Product.objects.all()

    myFilter = ProductFilter(request.GET, queryset=products)
    student = myFilter.qs

    context = {
        'products': products,
        'myFilter': myFilter,
    }
    return render(request, "ewalletAdmin/products.html", context)


def createProduct(request):

    product_form = ProductForm()
    if request.method == 'POST':
        product_form = ProductForm(request.POST)
        if product_form.is_valid():
            product_form.save()
            return redirect('/admin2/products/')

    # if a GET (or any other method) we'll create a blank form
    else:
        product_form = ProductForm()

    context = {
        'product_form': product_form,
    }
    return render(request, "ewalletAdmin/product_form.html", context)


def updateProduct(request, pk):
    product = Product.objects.get(id=pk)

    product_form = ProductForm(instance=product)
    if request.method == 'POST':
        product_form = ProductForm(request.POST, instance=product)
        if product_form.is_valid():
            product_form.save()
            return redirect('/admin2/products/')

    context = {
        'product_form': product_form,
    }
    return render(request, "ewalletAdmin/product_form.html", context)


def deleteProduct(request, pk):
    product = Product.objects.get(id=pk)

    if request.method == 'POST':
        product.delete()
        return redirect('/admin2/products/')

    context = {
        'item': product,
    }
    return render(request, "ewalletAdmin/delete.html", context)

# Transaction Model Views


class TransactionCreateView(CreateView):
    model = Transaction
    fields = [
        's_wallet',
        'amount'
    ]

    template_name = 'ewalletAdmin/transaction_form.html'
    success_url = "/admin2/transactions/"


def processTransaction(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    parent = request.user.parent
    p_wallet = parent.parentwallet
    s_wallet = StudentWallet.objects.get(id=data['form']['s_wallet'])

    if (s_wallet.balance > float(data['form']['amount'])):
        s_wallet.balance -= float(data['form']['amount'])
        s_wallet.save()

        Transaction.objects.create(
            s_wallet=s_wallet,
            transaction_id=transaction_id,
            timestamp=datetime.datetime.now(),
            transaction_type='Scan & Pay',
            description='Co-op',
            amount=data['form']['amount'],
        )
        return JsonResponse('Payment Complete', safe=False)

    else:
        return JsonResponse('Not enough balance', safe=False)


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


def transactions(request):
    transactions = Transaction.objects.all()

    myFilter = TransactionFilter(request.GET, queryset=transactions)
    transactions = myFilter.qs

    context = {
        'transactions': transactions,
        'myFilter': myFilter,
    }
    return render(request, "ewalletAdmin/transactions.html", context)
