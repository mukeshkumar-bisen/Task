from django.shortcuts import render, redirect
from django.views import View
from app.models import Customer, Product, Cart, OrderPlace
from app.forms import customerregistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
# for function based views
from django . contrib.auth.decorators import login_required
from django . utils.decorators import method_decorator  # for class based view
# def home(request):
#  return render(request, 'app/home.html')


class PrductView(View):
    def get(self, request):
        totalitems = 0
        topwear = Product.objects.filter(category="TW")
        bottomwear = Product.objects.filter(category="BW")
        mobile = Product.objects.filter(category="M")
        laptop = Product.objects.filter(category="L")
        if request.user.is_authenticated:
            totalitems = len(Cart.objects.filter(user=request.user))

        return render(request, 'app/home.html',  {'topwear': topwear, 'bottomwear': bottomwear, 'mobile': mobile, 'laptop': laptop, 'totalitems': totalitems})

# def product_detail(request):
#  return render(request, 'app/productdetail.html')


class ProductDetailView(View):
    def get(self, request, pk):  # here pk is the primary key
        totalitems = 0
        product = Product.objects.get(pk=pk)
        item_alredy_in_cart = False
        if request.user.is_authenticated:
            totalitems = len(Cart.objects.filter(user=request.user))
            item_alredy_in_cart = Cart.objects.filter(
                Q(product=product.id) & Q(user=request.user)).exists()

        return render(request, 'app/productdetail.html',
                      {'product': product, 'item_alredy_in_cart': item_alredy_in_cart, 'totalitems': totalitems})


@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')
    # return render(request, 'app/addtocart.html')


@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 70.0
        totalamount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
                totalamount = amount + shipping_amount
            return render(request, 'app/addtocart.html',
                          {'carts': cart,
                           'totalamount': totalamount, 'amount': amount})
        else:
            return render(request, 'app/empty.html')


def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)


def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user ==
                        request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)


def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user ==
                        request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount

        data = {
            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)


def buy_now(request):
    return render(request, 'app/buynow.html')


def profile(request):
    return render(request, 'app/profile.html')


def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', {"add": add, 'active': 'btn-primary'})


def orders(request):
    return render(request, 'app/orders.html')

# def change_password(request):
#  return render(request, 'app/changepassword.html')


def mobile(request, data=None):
    if data == None:
        mobile = Product.objects.filter(category="M")
    elif data == "Redmi" or data == "Samsung":
        mobile = Product.objects.filter(category="M").filter(brand=data)
    elif data == "below":
        mobile = Product.objects.filter(
            category="M").filter(discounted_price__lt=10000)
    elif data == "above":
        mobile = Product.objects.filter(
            category="M").filter(discounted_price__gt=10000)
    return render(request, 'app/mobile.html', {'mobile': mobile})

# def login(request):
#  return render(request, 'app/login.html')

# def customerregistration(request):
#  return render(request, 'app/customerregistration.html')


class CustomerRegistrationView(View):
    def get(self, request):
        form = customerregistrationForm()
        return render(request, 'app/customerregistration.html', {"form": form})

    def post(self, request):
        form = customerregistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, "Customer registration successfully...")
            form.save()
        return render(request, 'app/customerregistration.html', {"form": form})


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html',
                      {'form': form, 'active': 'btn-primary'})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']

            reg = Customer(
                user=usr,
                name=name,
                locality=locality,
                city=city,
                state=state,
                zipcode=zipcode,
                #  mobile = mobile
            )
            reg.save()
            messages.success(
                request, 'Congratualation!! Profile Update Successfully')
        return render(request, 'app/profile.html',
                      {'form': form, 'active': 'btn-primary'})


@login_required
def checkout(request):
    totalitems = 0
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    totalamount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if request.user.is_authenticated:
        totalitems = len(Cart.objects.filter(user=request.user))

    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        totalamount = amount + shipping_amount
    return render(request, 'app/checkout.html', {'totalitems': totalitems, 'add': add, 'totalamount': totalamount, 'cart_items': cart_items})


@login_required
def orders(request):
    op = OrderPlace.objects.filter(user=request.user)

    return render(request, 'app/orders.html', {'order_placed': op})


@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for i in cart:
        OrderPlace(customer=customer, user=user,
                   product=i.product, quantity=i.quantity).save()
        i.delete()

    return redirect("orders")
