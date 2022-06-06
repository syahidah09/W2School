import json
import calendar
from datetime import date, datetime, timedelta

import pytz
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.core import serializers
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from ewallet.decorators import *
from ewallet.models import *

from .filters import *
from .forms import *
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
    return redirect('/')


@login_required(login_url='/admin2/login/')
def homepage(request):
    transaction = Transaction.objects.filter(
        transaction_type="Payment", description="Co-op")
    student = Student.objects.all()
    parent = Parent.objects.all()
    transaction_allpayemnt = Transaction.objects.filter(
        transaction_type="Payment")
    total = sum([item.amount for item in transaction_allpayemnt])
    total = "{:.2f}".format(total)

    # total money spent by students class
    class_name = ("1A", "1B", "2A", "2B", "3A", "3B", "4A", "4B", "5A", "5B",)
    transaction_by_class = {}
    for i in class_name:
        transaction_by_class[i] = 0
    print(transaction_by_class)

    for i in transaction:
        print(i.student.class_name)
        s_class = i.student.class_name
        test = transaction_by_class.get(s_class)
        # print("S_class: ", s_class, "S_name: ", i.student, "Amount: ", i.amount, "Total spent in class: ", test, )
        transaction_by_class[s_class] = test + i.amount
    print(transaction_by_class)

    MY = pytz.timezone('Asia/Kuala_Lumpur')
    today = datetime.now(MY)
    sales_by_month = {}
    for x in range(1, 13):
        # get all transaction this year for each month
        tr = Transaction.objects.filter(
            date__year=today.year, date__month=x, transaction_type="Payment")
        amount = 0
        for j in tr:
            amount += j.amount
        sales_by_month[calendar.month_abbr[x]] = amount
    print(today.month+2)
    print(today.year)
    print(sales_by_month)

    context = {
        'transaction': transaction,
        'student': student,
        'parent': parent,
        'total': total,
        'test': transaction_by_class,
        'test2': sales_by_month,
        'year': today.year,
    }
    return render(request, "ewalletAdmin/home.html", context)

# -------------- Student Views --------------


# class StudentCreateView(CreateView):
#     model = Student
#     fields = '__all__'
#     template_name = 'ewalletAdmin/student_form.html'
#     success_url = "/admin2/students/"


def StudentCreateView2(request, pk):
    User = get_user_model()
    user = User.objects.get(id=pk)
    print("pk", pk)
    # print(parent)
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
        # initial={'parent': parent}
        if pk == 1:
            parent = user.parent
            form = StudentForm(initial={'parent': parent})
        else:
            form = StudentForm()

    context = {
        'form': form,
    }
    return render(request, "ewalletAdmin/student_form.html", context)


# class StudentListView(ListView):
#     model = Student
#     template_name = 'ewalletAdmin/student_list.html'
#     paginate_by = 15
    # context_object_name = 'classgroup'

    # def get_queryset(self):
    #     return Student.objects.filter(classgroup='5 Sina')

def StudentListView2(request):
    student = Student.objects.all()
    student_filter = StudentFilter(request.GET, queryset=student)

    context = {
        'student': student,
        'filter': student_filter,
    }
    return render(request, 'ewalletAdmin/student_list.html', context)


class StudentDetailView(DetailView):
    model = Student
    fields = ('student_id', 'first_name', 'last_name',
              'class_name', 'parent', 'card_id')
    template_name = 'ewalletAdmin/student_detail.html'


class StudentUpdateView(UpdateView):
    model = Student
    fields = ('student_id', 'first_name', 'last_name',
              'class_name', 'parent', 'card_id')
    template_name = 'ewalletAdmin/student_form.html'
    success_url = "/admin2/students/"


class StudentDeleteView(DeleteView):
    model = Student
    fields = '__all__'
    template_name = 'ewalletAdmin/student_confirm_delete.html'
    success_url = "/admin2/students/"


# -------------- User/Parent Views --------------


class ParentCreateView(CreateView):
    model = Parent
    fields = '__all__'
    template_name = 'ewalletAdmin/parent_form.html'
    success_url = "/admin2/parents/"


# class ParentListView(ListView):
#     model = Parent
#     template_name = 'ewalletAdmin/parent_list.html'
#     paginate_by = 15
    # context_object_name = 'classgroup'

    # def get_queryset(self):
    #     return Student.objects.filter(classgroup='5 Sina')

def ParentListView2(request):
    User = get_user_model()
    user = User.objects.filter(groups__name='parent')
    user_filter = UserFilter(request.GET, queryset=user)
    user = user_filter.qs

    context = {
        'user': user,
        'filter': user_filter,
    }
    return render(request, "ewalletAdmin/parent_list.html", context)


def ParentDetailView2(request, pk):
    User = get_user_model()
    user = User.objects.get(id=pk)
    student = user.parent.student_set.all()
    context = {
        'user': user,
        'student': student,
    }
    return render(request, "ewalletAdmin/parent_detail.html", context)


class ParentUpdateView(UpdateView):
    model = Parent
    fields = [
        'phone',
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


# class ProductListView(ListView):
#     model = Product
#     template_name = 'ewalletAdmin/product_list.html'
#     paginate_by = 10
    # context_object_name = 'classgroup'

    # def get_queryset(self):
    #     return Student.objects.filter(classgroup='5 Sina')

   # paginator = Paginator(product, 10)
    # try:
    #     product = paginator.page(page)
    # except EmptyPage:
    #     # if we exceed the page limit we return the last page
    #     product = paginator.page(paginator.num_pages)

def ProductListView2(request, page=1):
    product = Product.objects.all()
    product_filter = ProductFilter(request.GET, queryset=product)
    product = product_filter.qs
    context = {
        'product': product,
        'filter': product_filter,
    }
    return render(request, 'ewalletAdmin/product_list.html', context)


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


# class TransactionListView(ListView):
#     model = Transaction
#     template_name = 'ewalletAdmin/transaction_list.html'
#     paginate_by = 10
    # context_object_name = 'classgroup'

    # def get_queryset(self):
    #     return Student.objects.filter(classgroup='5 Sina')

def TransactionListView2(request):
    transaction = Transaction.objects.all()
    transaction_filter = TransactionFilter(request.GET, queryset=transaction)
    transaction = transaction_filter.qs

    page = request.GET.get('page', 1)
    paginator = Paginator(transaction, 10)
    
    try:        
        transaction = paginator.page(page)        
    except PageNotAnInteger:
        transaction = paginator.page(1)
    except EmptyPage:        
        # if we exceed the page limit we return the last page
        transaction = paginator.page(paginator.num_pages)

    context = {
        'transaction': transaction,
        'filter': transaction_filter,
    }
    return render(request, 'ewalletAdmin/transaction_list.html', context)


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


# class OrderListView(ListView):
#     model = Order
#     template_name = 'ewalletAdmin/order_list.html'
#     paginate_by = 10

def OrderListView2(request):
    order = Order.objects.all()
    order_filter = OrderFilter(request.GET, queryset=order)
    order = order_filter.qs

    context = {
        'order': order,
        'filter': order_filter,
    }
    return render(request, 'ewalletAdmin/order_list.html', context)


class OrderUpdateView(UpdateView):
    model = Order
    fields = ['receive', ]
    template_name = 'ewalletAdmin/order_form.html'
    success_url = "/admin2/orders/"
