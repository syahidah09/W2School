import json
import os,math
from datetime import date, datetime, timedelta
from io import BytesIO

import pytz
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.core.paginator import EmptyPage, Paginator
from django.http import response
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import DetailView, ListView, UpdateView
from reportlab.lib.colors import *
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (Paragraph, SimpleDocTemplate, Spacer, Table,
                                TableStyle)

from .decorators import *
from .filters import *
from .forms import *
from .models import *


@unauthenticated_user
def frontPage(request):
    context = {}
    return render(request, "partials/frontpage.html", context)


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
    return redirect('/')


@login_required(login_url='/login/')
def user_detail(request):
    user = request.user
    parent = user.parent
    context = {
        'parent': parent,
        'user': user
    }
    return render(request, "ewallet/user_detail.html", context)

MY = pytz.timezone('Asia/Kuala_Lumpur')
today = datetime.now(MY)
date = "2022-01-18 18:44:12.726799+08:00"
@login_required(login_url='/login/')
def user_update(request):
    user = request.user
    parent = user.parent
    parent_form = ParentForm(instance=parent)
    user_form = UserForm(instance=user)

    if request.method == 'POST':
        parent_form = ParentForm(request.POST, instance=parent)
        user_from = UserForm(request.POST, instance=user)
        if parent_form.is_valid():
            parent_form.save()
            user_from.save()
            return redirect('/user_profile/')

    context = {
        'parent_form': parent_form,
        'user_form': user_form
    }
    return render(request, "ewallet/user_form.html", context)


@login_required(login_url='/login/')
def homepage(request):
    parent = request.user.parent
    student = parent.student_set.all()
    transaction = parent.transaction_set.all()[:5]    
    tr=[]
    for i in parent.transaction_set.all()[:3]:
        tr.append(i)
        for j in student:
            for k in j.transaction_set.all()[:3]:
                tr.append(k)
    for i in tr[:5]:
        print(i.description)
    ltr=[]
    for i in student:
        s=[]
        amount=0        
        s.append(i.first_name)        
        tr=i.transaction_set.filter(date__month=today.month)
        for j in tr:
            amount+=j.amount
        s.append(math.ceil(amount))
        ltr.append(s)        

    context = {
        'parent': parent,
        'student': student,
        'transaction': tr[:5],
        'ltr':ltr,
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
        details = TransferForm(request.POST)       
        if details.is_valid():            
            post = details.save(commit=False)            
            post.save()
            return HttpResponse("data submitted successfully")
        else:
            return HttpResponse("data invalid")        

    else:    
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
        form.fields["student"].queryset = student

        context = {
            'form': form,
            'myOption': myOption,
            'parent': parent,
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
        transactions = paginator.page(paginator.num_pages)

    context = {
        'transactions': transactions,
        'filter': myFilter,
    }
    return render(request, "ewallet/transaction_list.html", context)


@login_required(login_url='/login/')
def transaction_detail(request, pk):
    tr = Transaction.objects.get(id=pk)

    item = None
    if tr.order is not None:
        item = tr.order.orderitem_set.all()
        print(tr.order.id)
    print(item)

    context = {
        'transaction': tr,
        'item': item,
    }
    return render(request, "ewallet/transaction_detail.html", context)

@login_required(login_url='/login/')
def store(request):
    parent = request.user.parent
    order, created = Order.objects.get_or_create(
        parent=parent, complete=False, date_ordered=date)
    cartItems = order.get_cart_items   
    products = Product.objects.all()
    myFilter = ProductFilter(request.GET, queryset=products)   

    context = {
        'products': products,
        'cartItems': cartItems,
        'filter': myFilter,
    }
    return render(request, "ewallet/store.html", context)


@login_required(login_url='/login/')
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    # print('Action:', action)
    # print('productId:', productId)

    parent = request.user.parent
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(
        parent=parent, complete=False, date_ordered=date)

    orderItem, created = OrderItem.objects.get_or_create(
        order=order, product=product,date_added=date)

    # print("[updateitem] Order ID: ", order.id)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


@login_required(login_url='/login/')
def cart(request):
    parent = request.user.parent
    order = Order.objects.get(
        parent=parent, complete=False, date_ordered=date)
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
        parent=parent, complete=False,date_ordered=date)
    items = order.orderitem_set.all()
    cartItems = order.get_cart_items
   
    if request.method == 'POST':
        details = TransactionForm(request.POST)      
        if details.is_valid():
            post = details.save(commit=False)
            order.student = Student.objects.get(
                student_id=request.POST.get('student'))
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
            'parent': parent,
        }
        return render(request, 'ewallet/checkout.html', context)


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
    # print("[processorder] Order ID: ", order.id)
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
    # print(student)
    order = Order.objects.get(
        parent=parent,
        complete=False)  # temp True
    total = float(data['form']['total'])   # total is null here
    # print("[processTransaction] Order ID: ", order.id)
    # print("Get cart total: ", order.get_cart_total)
    if total == order.get_cart_total:
        order.student = student
        order.complete = True  # not set to true after payment w mywallet on checkout page
        # print("trueeee")
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
    transaction_id = datetime.now().timestamp()
    data = json.loads(request.body)

    parent = request.user.parent
    parent.wallet_balance += float(data['form']['amount'])
    parent.save()

    Transaction.objects.create(
        parent=parent,
        transaction_id=transaction_id,
        date=datetime.now(),
        transaction_type='Deposit',
        amount=data['form']['amount'],
    )
    return JsonResponse('Payment Complete', safe=False)


@login_required(login_url='/login/')
def processReload(request):
    transaction_id = datetime.now().timestamp()
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
            date=datetime.now(),
            transaction_type='Transfer',
            amount=data['form']['amount'],
        )
        return JsonResponse('Payment Complete', safe=False)

    else:
        return JsonResponse('Not enough balance', safe=False)

# refered https://medium.com/@saijalshakya/generating-pdf-with-reportlab-in-django-ee0235c2f133 & https://eric.sau.pe/reportlab-and-django-part-1-the-set-up-and-a-basic-example


def download_receipt(request, pk):
    transactions = Transaction.objects.get(id=pk)

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

    if transactions.description is not None:
        DetailTable = Table([
            ["Name", ":",  transactions.parent],
            ["Student Name", ":",  transactions.student],
            ["Description", ":", transactions.description]
        ], [70, 10, 150])
    else:
        DetailTable = Table([
            ["Name", ":",  transactions.parent],
            ["Description", ":", transactions.description]
        ], [70, 10, 150])

    InvoiceDetailTable = Table([
        [InvoiceTable, DetailTable],
    ])

    if transactions.description is not None:
        items = transactions.order.orderitem_set.all()
        data = [["No.", "Product", "Quantity",
                 "Unit Price (RM)", "Total (RM)"], ]
        count = 0
        for i in items:
            count += 1
            data.append([
                count, i.product, i.quantity,
                "{:.2f}".format(i.product.price), "{:.2f}".format(i.get_total),
            ])
        ProdcuctTable = Table(data, [60, 400, 60, 80, 60])
    else:
        data = [["No.", "Transaction Type", "Amount (RM)"], ]
        data.append([
            "1", transactions.transaction_type, transactions.amount,
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

    if transactions.description is not None:
        Total = Paragraph(text=("Total: RM %.2f" %
                                (transactions.order.get_cart_total)), style=TotalStyle)
    else:
        Total = Paragraph(text=(""), style=TotalStyle)

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
