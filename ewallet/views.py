from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages
from django.views.generic import ListView, DetailView, UpdateView
from django.core.paginator import Paginator, EmptyPage


from .models import *
from .forms import *
from .filters import *
from .decorators import *
import datetime
import json


@unauthenticated_user
def frontPage(request):
    context = {}
    return render(request, "ewallet/frontpage.html", context)


@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CreateUserForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')

            group, created = Group.objects.get_or_create(name='parent')
            print("Group id: " + str(group))
            user.groups.add(group)

            Parent.objects.create(
                user=user,
                name=user.username,
                email=email,
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

        if (user is not None) and (user.groups.filter(name="parent")):
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
def user_detail(request):
    parent = request.user.parent
    context = {
        'parent': parent
    }
    return render(request, "ewallet/user_detail.html", context)


@login_required(login_url='/login/')
def user_update(request):
    parent = request.user.parent
    parent_form = ParentForm(instance=parent)

    if request.method == 'POST':
        parent_form = ParentForm(request.POST, instance=parent)
        if parent_form.is_valid():
            parent_form.save()
            return redirect('/user_profile/')

    context = {
        'parent_form': parent_form
    }
    return render(request, "ewallet/user_form.html", context)


@login_required(login_url='/login/')
def homepage(request):
    user = request.user

    if not user.groups.filter(name="parent"):
        print("User " + user.username + " is NOT in a group parent")
        messages.info(request, 'You need to login with a non-admin account')
        logout(request)
        return redirect('/')

    parent = user.parent
    student = parent.student_set.all()
    transactions = user.parent.transaction_set.all()[:5]

    context = {
        'parent': parent,
        'student': student,
        'transactions': transactions,
    }
    return render(request, "ewallet/home.html", context)


@login_required(login_url='/login/')
def wallet_page(request):
    parent = request.user.parent
    student = parent.student_set.all()

    context = {
        'parent': parent,
        'student': student,
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
    user = request.user
    parent = user.parent
    student = parent.student_set.all()

    myOption = StudenttFilter(request.GET, queryset=student)
    s = myOption.qs

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
        # filter only this user's child
        form.fields["student"].queryset = student

        context = {
            'form': form,
            'myOption': myOption,
            's': s,
        }
        return render(request, "ewallet/reload.html", context)


@login_required(login_url='/login/')
def transaction_history(request, page=1):
    transactions = request.user.parent.transaction_set.all()
    paginator = Paginator(transactions, 8)  # 10 transactions per page

    print(request.user.parent.student_set.all())
    myFilter = TransactionFilter(request.GET, queryset=transactions)
    transactions = myFilter.qs

    try:
        transactions = paginator.page(page)
    except EmptyPage:
        # if we exceed the page limit we return the last page
        transactions = paginator.page(paginator.num_pages)

    context = {
        'transactions': transactions,
        'myFilter': myFilter,
    }
    return render(request, "ewallet/transaction_list.html", context)


@login_required(login_url='/login/')
def store(request):
    parent = request.user.parent
    order, created = Order.objects.get_or_create(
        parent=parent, complete=False)
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
    order = Order.objects.get(
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
    student = parent.student_set.all()

    order = Order.objects.get(
        parent=parent, complete=False)
    items = order.orderitem_set.all()
    cartItems = order.get_cart_items

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
        form.fields["student"].queryset = student

        context = {
            'form': form,
            'items': items,
            'order': order,
            'cartItems': cartItems,
            'student': student,
            'parent': parent,
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

# Pay w Paypal at checkout


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

    return JsonResponse('Payment Complete', safe=False)

# Pay w MyWallet at checkout


@login_required(login_url='/login/')
def processTransaction(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    parent = request.user.parent
    parent.wallet_balance -= float(data['form']['amount'])
    parent.save()
    student = Student.objects.get(student_id=data['form']['student'])

    order, created = Order.objects.get_or_create(
        parent=parent, complete=False)
    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    Transaction.objects.create(
        parent=parent,
        student=student,
        transaction_id=transaction_id,
        date=datetime.datetime.now(),
        transaction_type='Payment',
        description='e-Store',
        amount=data['form']['amount'],
    )
    return JsonResponse('Payment Complete', safe=False)


@login_required(login_url='/login/')
def processTopup(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    parent = request.user.parent
    parent.wallet_balance += float(data['form']['amount'])
    parent.save()

    Transaction.objects.create(
        parent=parent,
        transaction_id=transaction_id,
        date=datetime.datetime.now(),
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
    student = Student.objects.get(student_id=data['form']['student'])

    if (parent.wallet_balance > 0.0):
        parent.wallet_balance -= float(data['form']['amount'])
        parent.save()
        student.wallet_balance += float(data['form']['amount'])
        student.save()

        Transaction.objects.create(
            parent=parent,
            student=student,
            transaction_id=transaction_id,
            date=datetime.datetime.now(),
            transaction_type='Transfer',
            description='Reload',
            amount=data['form']['amount'],
        )
        return JsonResponse('Payment Complete', safe=False)

    else:
        return JsonResponse('Not enough balance', safe=False)
