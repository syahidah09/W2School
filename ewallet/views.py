from django.http import response
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages
from django.views.generic import ListView, DetailView, UpdateView
from django.core.paginator import Paginator, EmptyPage

from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.units import cm
from reportlab.lib.colors import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO


from .models import *
from .forms import *
from .filters import *
from .decorators import *
import datetime
import json
import os


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

            group, created = Group.objects.get_or_create(name='parent')
            print("Group id: " + str(group))
            user.groups.add(group)

            Parent.objects.create(
                user=user,                
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
    user = request.user
    parent = user.parent
    context = {
        'parent': parent,
        'user': user
    }
    return render(request, "ewallet/user_detail.html", context)


@login_required(login_url='/login/')
def user_update(request):
    user = request.user
    parent = user.parent
    parent_form = ParentForm(instance=parent)
    user_from = UserForm(instance=user)

    if request.method == 'POST':
        parent_form = ParentForm(request.POST, instance=parent)
        user_from = UserForm(request.POST, instance=user)
        if parent_form.is_valid():
            parent_form.save()
            user_from.save()
            return redirect('/user_profile/')

    context = {
        'parent_form': parent_form,
        'user_from': user_from
    } 
    return render(request, "ewallet/user_form.html", context)


@login_required(login_url='/login/')
def homepage(request):
    user = request.user
    parent = user.parent
    student = parent.student_set.all()
    transactions = user.parent.transaction_set.all()[:5]

    if not user.groups.filter(name="parent"):
        print("User " + user.username + " is NOT in a group parent")
        messages.info(request, 'You need to login with a non-admin account')
        logout(request)
        return redirect('/')

    context = {
        'user': user,
        'parent': parent,
        'student': student,
        'transactions': transactions,
    }
    return render(request, "ewallet/home.html", context)


@login_required(login_url='/login/')
def wallet_page(request):
    user = request.user
    parent = user.parent
    student = parent.student_set.all()

    context = {
        'user': user,
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
    paginator = Paginator(transactions, 10)  # 10 transactions per page
    
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


def TransactionDetail(request, pk):
    tr = Transaction.objects.get(id=pk)

    items = None
    if tr.order is not None:
        items = tr.order.orderitem_set.all()    

    context = {
        'transaction': tr,
        'items': items,
    }
    return render(request, "ewallet/transaction_detail.html", context)


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
        parent=parent,
        student=student,
        complete=True)  # temp True
    total = float(data['form']['total'])   # total is null here

    if total == order.get_cart_total:
        order.complete = True  # not set to true after payment w mywallet on checkout page
    order.save()

    Transaction.objects.create(
        parent=parent,
        student=student,
        transaction_id=transaction_id,
        date=datetime.datetime.now(),
        transaction_type='Payment',
        description='e-Store',
        amount=data['form']['amount'],
        order=order
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

# refered https://medium.com/@saijalshakya/generating-pdf-with-reportlab-in-django-ee0235c2f133 & https://eric.sau.pe/reportlab-and-django-part-1-the-set-up-and-a-basic-example
def download_receipt(request, pk):
    transactions = Transaction.objects.get(id=pk)    
    items = transactions.order.orderitem_set.all()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="receipt.pdf"'

    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=landscape(A4))

    styles = getSampleStyleSheet()
    story = []

    # Title
    styleT = styles['Title']
    story.append(Paragraph("Invoice/Receipt", styleT))
    space = Spacer(cm, 0.8*cm)

    # Build structure
    InvoiceTable = Table([
        ["Invoice No.", ":",  transactions.transaction_id],
        ["Invoice Date", ":", transactions.date.strftime("%d/%m/%Y")]
    ], [60, 10, 150])

    DetailTable = Table([
        ["Name", ":",  transactions.parent],
        ["Description", ":", transactions.description]
    ], [60, 10, 150])

    InvoiceDetailTable = Table([
        [InvoiceTable, DetailTable],
    ])

    data=[["No.", "Product", "Quantity", "Unit Price (RM)", "Total (RM)"],]
    count=0
    for i in items:
        count+=1        
        data.append([
            count, i.product, i.quantity,
                "{:.2f}".format(i.product.price), "{:.2f}".format(i.get_total),
                ])    
    ProdcuctTable = Table(data, [60, 400, 60, 80, 60])    

    ElemTable = Table([
        [InvoiceDetailTable],
        [space],
        [ProdcuctTable],
    ])

    # Paragraph
    TotalStyle = ParagraphStyle(
        name='Normal',
        alignment=2,
        spaceAfter=6,
        spaceBefore=6,
        rightIndent=20
    )

    NoteStyle = styles['BodyText']
    NoteStyle.textColor = gray
    NoteStyle.leftIndent = 10
    OrgStyle = styles['Heading5']
    OrgStyle.alignment = 1

    Total = Paragraph(text =("Total: RM %.2f"% (transactions.order.get_cart_total)), style=TotalStyle)

    Note = Paragraph(''' 
        Note: This receipt is computer generated and no signature is required
    ''', NoteStyle)

    Org = Paragraph(''' 
        Wallet2School
    ''', OrgStyle)

    # Add table style
    InvoiceTableStyle = TableStyle(
        [
            ("TEXTCOLOR", (0, 0), (0, 2), darkblue),
        ]
    )
    InvoiceTable.setStyle(InvoiceTableStyle)
    DetailTable.setStyle(InvoiceTableStyle)

    ProdcuctTableStyle = TableStyle(
        [
            ("BOX", (0, 0), (-1, -1), 1, black),
            ("GRID", (0, 0), (4, 4), 1, black),
            ("BACKGROUND", (0, 0), (4, 0), cornflowerblue),
            ("TEXTCOLOR", (0, 0), (-1, 0), black),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("BACKGROUND", (0, 1), (-1, -1), lightcyan),
        ]
    )
    ProdcuctTable.setStyle(ProdcuctTableStyle)

    ElemTable2 = Table([
        [ElemTable],
        [Total],
        [space],
        [Note],
        [space],
        [Org]
    ])

    story.append(ElemTable2)
    doc.build(story)
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response