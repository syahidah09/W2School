from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages

from .models import ParentWallet, StudentWallet, Student, Parent, Transaction
from ewalletAdmin.models import Product
from .forms import StudentForm, CreateUserForm
from .filters import TransactionFilter
from .decorators import unauthenticated_user

# @unauthenticated_user


def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CreateUserForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get_or_create(name='parent')
            user.groups.add(group)

            Parent.objects.create(
                user=user,
                name=user.username,
            )
            ParentWallet.objects.create(
                parent=user.parent,
            )

            messages.success(
                request, 'Your account was created succesfully, ' + username)
            return redirect('/login/')

    context = {'form': form}
    return render(request, "ewallet/register.html", context)


@unauthenticated_user
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


def logoutUser(request):
    logout(request)
    return redirect('/login/')


@login_required(login_url='/login/')
def homepage(request):
    user = request.user
    pw = user.parent.parentwallet.balance
    sw = user.parent.studentwallet_set.all()
    transactions = Transaction.objects.all()

    # print('The user name is '+ user.parent.name)
    # print('Parent wallet: '+ pw.parent.name)
    # print('Student wallet: '+ s_wallet.explain())

    context = {
        'pw': pw,
        'sw': sw,
        'transactions': transactions,
    }
    return render(request, "ewallet/home.html", context)


@login_required(login_url='/login/')
def wallet_page(request):
    user = request.user
    pwb = user.parent.parentwallet.balance
    sw = user.parent.studentwallet_set.all()

    if request.method == 'POST':
        num = request.POST['amount']
        id = request.POST['studentID']
        if num != 0 and pwb != 0:
            student = Student.objects.filter(
                student_id=id)
            a = pwb - float(num)
            b = student.studentwallet.balance + float(num)            
            return redirect('/wallet/')

        else:
            messages.info(request, 'Not enough money to transfer')

    context = {
        'pwb': pwb,
        'sw': sw,
        # 'student': student,
    }

    return render(request, "ewallet/wallet.html", context)


# @login_required(login_url='/login/')
# def topup_page(request):
#     return render(request, "ewallet/topup.html", {})


@login_required(login_url='/login/')
def py(request):
    transactions = Transaction.objects.all()

    myFilter = TransactionFilter(request.GET, queryset=transactions)
    transactions = myFilter.qs

    context = {
        'transactions': transactions,
        'myFilter': myFilter,
    }
    return render(request, "ewallet/transaction_history.html", context)


@login_required(login_url='/login/')
def add_dependent(request):
    student_form = StudentForm()

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        student_form = StudentForm(request.POST)
        # check whether it's valid:
        if student_form.is_valid():
            student_form.save()
            return redirect('/wallet/')

    # if a GET (or any other method) we'll create a blank form
    else:
        student_form = StudentForm()

    context = {
        'student_form': student_form,
    }
    return render(request, "ewallet/add_dependent.html", context)


@login_required(login_url='/login/')
def store(request):
    products = Product.objects.all()

    context = {
        'products': products,
    }
    return render(request, "ewallet/store.html", context)
