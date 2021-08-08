from django.http import JsonResponse
from django.shortcuts import render, redirect
from products.models import Category,ConfeirmCode
from products.models import Product
from products.forms import ProductForm,RegisterForm
from  django.contrib import auth
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
import datetime
categories = Category.objects.all()

def category_vievs(request,Category_id):
    prod = Product.objects.filter(category_id=Category_id)
    category = Category.objects.all()
    produts = Product.objects.all()

    data = {
        "product_list": prod,
        "Category_list": category,
        "Product_list": produts
    }
    return render(request, "item.html", context=data)

PAGE_SIZE=7
def main_page_view(request):
    page = int(request.GET.get("page", "1"))
    print("Страница:", page)
    print(f"Обьекты :[{(page - 1 * PAGE_SIZE)}:{page * PAGE_SIZE} ]")
    products = Product.objects.all()
    total = products.count()
    page_count = total // PAGE_SIZE
    if total % PAGE_SIZE > 0:
        page_count = page_count + 1
    next_page = page + 1
    prev_page = page - 1
    data = {
        "title": "Главная страница",
        "page": page,
        "page_count": range(1, page_count + 1),
        "next_page": next_page,
        "prev_page": prev_page,
        "last_page": page_count,
        "product_list": products[(page - 1) * PAGE_SIZE:page * PAGE_SIZE],
        "Category_list": categories,
        "Product_list": products
    }
    return render(request, "index.html", context=data)

def product_item_view(request,Product_id):
    product = Product.objects.get(id=Product_id)
    category = Category.objects.all()
    produts = Product.objects.all()
    data={
        "product":product,
        "Category_list": category,
        "Product_list": produts
    }
    return render(request, "product.html", context=data)

@login_required(login_url="/login/")
def add_product(request):
    if request.method =="GET":
        data={
            "form": ProductForm
        }
        return render(request,"add.html",context=data)
    elif request.method=="POST":
        form=ProductForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")


def logout(request):
    auth.logout(request)
    return redirect("/login/")

def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("/")
    data = {
        "form": LoginForm()
    }
    return render(request, "Login.html", context=data)


def register(request):
    if request.method=="POST":
        form=RegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("/login/")
        else:
            data={
                "form":form
            }
            return render(request,"register.html",context=data)
    data = {
        "form": RegisterForm()
    }
    return render(request,"register.html",context=data)


def search(request):
    query=request.GET.get("query","")
    print(query)
    products=Product.objects.filter(title__contains=query)
    print(products.values())
    return JsonResponse(data={"list":list(products.values())},safe=False)


def javascript(request):
    return render(request,"javascript.html")


def activate(request,code):
    print(code)
    try:
        user=ConfeirmCode.objects.get(code=code,
                                      valid_until__gte=datetime.datetime.now()).user
        user.is_active = True
        user.save()
    except:
        pass
    return redirect("/login/")

