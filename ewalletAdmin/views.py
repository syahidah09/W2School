from django.shortcuts import render, redirect, HttpResponseRedirect

from ewallet.models import Parent, Student, Transaction
from ewallet.decorators import allowed_users
from .models import Product
from .forms import ProductForm, StudentForm
from .filters import TransactionFilter, StudentFilter, ProductFilter


@allowed_users(allowed_roles=['admin'])
def homepage(request):
    context = {

    }
    return render(request, "ewalletAdmin/home.html", context)


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


def transactions(request):
    transactions = Transaction.objects.all()

    myFilter = TransactionFilter(request.GET, queryset=transactions)
    transactions = myFilter.qs

    context = {
        'transactions': transactions,
        'myFilter': myFilter,
    }
    return render(request, "ewalletAdmin/transactions.html", context)
