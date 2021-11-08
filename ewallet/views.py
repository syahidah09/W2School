from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages

from .models import (
    Student,
    Parent,
    ParentWallet,
    StudentWallet,
    Transaction,
    Product,
    Order,
    OrderItem,
    ShippingAddress,
)
from .forms import StudentForm, CreateUserForm, TransferForm, ReloadForm
from .filters import TransactionFilter, SwalletFilter
from .decorators import unauthenticated_user
import datetime
import json

# @unauthenticated_user

def frontPage(request):
    context = {}
    return render(request, "ewallet/frontdoor.html", context)

def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CreateUserForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group, created = Group.objects.get_or_create(name='parent')
            print("Group id: " + str(group))
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

    if not user.groups.filter(name="parent"):
        print("User " + user.username + " is NOT in a group parent")
        messages.info(request, 'You need to login with a non-admin account')
        logout(request)
        return redirect('/login/')

    pw = user.parent.parentwallet.balance
    sw = user.parent.studentwallet_set.all()
    transactions = user.parent.transaction_set.all()

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

    # transaction = Transaction.objects.get_or_create(transaction_id=1, transaction_type='Deposit')

    context = {
        'pwb': pwb,
        'sw': sw,
        # 'student': student,
    }

    return render(request, "ewallet/wallet.html", context)


@login_required(login_url='/login/')
def topup_page(request):

    if request.method == 'POST':

        # Pass the form data to the form class
        details = TransferForm(request.POST)

        # In the 'form' class the clean function
        # is defined, if all the data is correct
        # as per the clean function, it returns true
        if details.is_valid():

            # Temporarily make an object to be add some
            # logic into the data if there is such a need
            # before writing to the database
            post = details.save(commit=False)

            # Finally write the changes into database
            post.save()
            return HttpResponse("data submitted successfully")

        else:
            return HttpResponse("data invalid")
        # return redirect('/topup/')
    else:

        # If the request is a GET request then,
        # create an empty form object and
        # render it into the page
        form = TransferForm(None)
        context = {'form': form}
        return render(request, "ewallet/topup.html", context)

@login_required(login_url='/login/')
def reload(request):
    sw = request.user.parent.studentwallet_set.all()
    pw = request.user.parent.parentwallet

    myOption = SwalletFilter(request.GET, queryset=sw)
    sw = myOption.qs

    if request.method == 'POST':        
        details = ReloadForm(request.POST)
        
        if details.is_valid():            
            post = details.save(commit=False)            
            post.save()
            return HttpResponse("data submitted successfully")

        else:
            return HttpResponse("data invalid")
       
    else:        
        form = ReloadForm(None)
        context = {
            'form': form,
            'myOption': myOption,
            'sw': sw,
            'pw': pw
        }
        return render(request, "ewallet/reload.html", context)

@login_required(login_url='/login/')
def transaction_history(request):
    transactions = request.user.parent.transaction_set.all()

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
    parent = request.user.parent
    order, created = Order.objects.get_or_create(
        parent=parent, complete=False)
    items = order.orderitem_set.all()
    cartItems = order.get_cart_items

    products = Product.objects.all()
    context = {
        'products': products,
        'cartItems': cartItems
    }
    return render(request, "ewallet/store.html", context)


@login_required(login_url='/login/')
def cart(request):
    parent = request.user.parent
    order, created = Order.objects.get_or_create(
        parent=parent, complete=False)
    items = order.orderitem_set.all()
    cartItems = order.get_cart_items

    context = {
        'items': items,
        'order': order,
        'cartItems': cartItems
    }
    return render(request, 'ewallet/cart.html', context)


@login_required(login_url='/login/')
def checkout(request):
    parent = request.user.parent
    order, created = Order.objects.get_or_create(
        parent=parent, complete=False)
    items = order.orderitem_set.all()
    cartItems = order.get_cart_items

    context = {
        'items': items,
        'order': order,
        'cartItems': cartItems
    }
    return render(request, 'ewallet/checkout.html', context)


@login_required(login_url='/login/')
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('productId:', productId)

    parent = request.user.parent
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(
        parent=parent, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(
        order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


@login_required(login_url='/login/')
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    parent = request.user.parent
    order, created = Order.objects.get_or_create(
        parent=parent, complete=False)
    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    ShippingAddress.objects.create(
        parent=parent,
        order=order,
        address=data['shipping']['address'],
        city=data['shipping']['city'],
        state=data['shipping']['state'],
        zipcode=data['shipping']['zipcode'],

    )
    return JsonResponse('Payment Complete', safe=False)


@login_required(login_url='/login/')
def processTransaction(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    parent = request.user.parent
    p_wallet = parent.parentwallet
    p_wallet.balance += float(data['form']['amount'])
    p_wallet.save()

    # if total == transaction.get_cart_total:
    #     transaction.complete = True
    # transaction.save()

    Transaction.objects.create(
        parent=parent,
        transaction_id=transaction_id,
        timestamp=datetime.datetime.now(),
        transaction_type='Deposit',
        description='Online',
        amount=data['form']['amount'],
    )
    return JsonResponse('Payment Complete', safe=False)

@login_required(login_url='/login/')
def processReload(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    parent = request.user.parent
    p_wallet = parent.parentwallet
    s_wallet = StudentWallet.objects.get(id=data['form']['s_wallet'])    

    print(type(p_wallet.balance))
    
    if (p_wallet.balance > 0.0):
        p_wallet.balance -= float(data['form']['amount'])
        p_wallet.save()
        s_wallet.balance += float(data['form']['amount'])
        s_wallet.save()  

        Transaction.objects.create(
            parent=parent,
            s_wallet= s_wallet,
            transaction_id=transaction_id,
            timestamp=datetime.datetime.now(),
            transaction_type='Transfer',
            description='Reload',
            amount=data['form']['amount'],
        )
        return JsonResponse('Payment Complete', safe=False)
    
    else:        
        return JsonResponse('Not enough balance', safe=False)
