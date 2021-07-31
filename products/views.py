from django.shortcuts import render, redirect
from .models import Product, Category
from products.forms import ProductForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from products.forms import RegisterForm
from .forms import LoginForm

# Create your views here.
def main_page_view(request):
    products = Product.objects.all()

    data = {
        'title': 'Главная страница',
        'products_list': products,


    }
    return render(request, "index.html", context=data)


def product_item_view(request, product_id):
    product = Product.objects.get(id=product_id)
    data = {
        'product': product,
        'title': product.title,
        'tags': product.tags,

    }
    return render(request, 'item.html', context=data)

def category_view(request):
    category = Category.objects.all()
    data = {
        'category_list': category,
    }
    return render(request, 'category.html', context=data)


@login_required(login_url='/login/')
def add_product(request):
    if request.method == 'GET':
        data = {
            'form' : ProductForm()
        }
        return render(request, 'add.html', context=data)
    elif request.method == 'POST':
        form = ProductForm (data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')


def logout(request):
    auth.logout(request)
    return redirect('/login/')

from .forms import LoginForm
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
    data = {
        'form': LoginForm(),

    }
    return render(request, 'login.html', context=data)

def register(request):
    if request.method == 'POST':
        form =RegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login/')
        else:
            data = {
                'form':form,
            }
            return render(request, 'register.html', context=data)
    data = {
        'form': RegisterForm()
    }
    return render(request, 'register.html', context=data)
