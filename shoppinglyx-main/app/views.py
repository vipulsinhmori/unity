
from.models import Customer, Product, Cart, OrderPlaced
from django.shortcuts import render, redirect # Make sure to import your form
from django.views import View
from .forms import CustomerRegistrationForm
from django.contrib import messages
from .forms import CustomerProfileForm
from django.http import JsonResponse
from django.db.models import Q
# from django.http import Http404
from django.http import HttpResponse, Http404
# from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
# from django.shortcuts import render
from .models import OrderPlaced
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import AnonymousUser

from django.views import View
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import AnonymousUser
from .models import Product, Cart


def mobile(request, data=None):
    if data == None:
        mobile=Product.objects.filter(category='M')
    elif data=='oneplus' or data=='Vivo':
        mobile=Product.objects.filter(category='M').filter(brand=data)
    elif data=='below':
         mobile=Product.objects.filter(category='M').filter(discounted_price__lt=10000)
    elif data=='above':
         mobile=Product.objects.filter(category='M').filter(discounted_price__gt=10000)
    return render(request, 'app/mobile.html', {'mobile': mobile})


def laptop(request, data=None):
 if data == None:
        laptop=Product.objects.filter(category='L')
 elif data=='lenevo' or data=='Asus':
        laptop=Product.objects.filter(category='L').filter(brand=data)
 elif data=='below':
         laptop=Product.objects.filter(category='L').filter(discounted_price__lt=10000)
 elif data=='above':
         laptop=Product.objects.filter(category='L').filter(discounted_price__gt=10000)
 return render(request, 'app/Laptop.html',{'laptop':laptop})

def topwears(request, data=None):
 if data == None:
        topwears=Product.objects.filter(category='TW')
 elif data=='T-shrit' or data=='AMERICANCREW':
        topwears=Product.objects.filter(category='TW').filter(brand=data)
 elif data=='below':
         topwears=Product.objects.filter(category='TW').filter(discounted_price__lt=5050)
 elif data=='above':
         topwears=Product.objects.filter(category='TW').filter(discounted_price__gt=600)
 return render(request, 'app/topwears.html',{'topwears':topwears})

def bottomwears(request, data=None):
 if data == None:
        bottomwears=Product.objects.filter(category='BW')
 elif data=='jeans5' or data=='pants':
        bottomwears=Product.objects.filter(category='BW').filter(brand=data)
 elif data=='below':
         bottomwears=Product.objects.filter(category='BW').filter(discounted_price__lt=400)
 elif data=='above':
         bottomwears=Product.objects.filter(category='BW').filter(discounted_price__gt=600)
 return render(request, 'app/bottomwears.html',{'bottomwears':bottomwears})

class ProductView(View):
    def get(self,request):
        topwears=Product.objects.filter(category='TW')
        bottomwears=Product.objects.filter(category='BW')
        mobile=Product.objects.filter(category='M')
        laptop = Product.objects.filter(category='L')

        return render(request,'app/home.html/',
        {'topwears':topwears,'bottomwears':bottomwears,'mobile':mobile, 'laptop': laptop})


# class ProductDetailView(View):
#     def get(self,request,pk):
#         product=Product.objects.get(pk=pk)
#         item_already_in_cart = False
#         item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
#         return render(request,'app/productdetail.html',{'product':product, ' item_already_in_cart': item_already_in_cart})


class ProductDetailView(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)

        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Get the actual user ID
            user_id = request.user.id

            # Now you can use user_id in your query
            item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=user_id)).exists()
        else:
            # If the user is not authenticated, set item_already_in_cart to False
            item_already_in_cart = False

        return render(request, 'app/productdetail.html', {'product': product, 'item_already_in_cart': item_already_in_cart})

@login_required        
def add_to_cart(request):
 user=request.user
 product_id = request.GET.get('prod_id')
 product = Product.objects.get(id=product_id)
 Cart(user=user,product=product).save()
 return redirect('/cart')


@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        print(cart)
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0

        cart_product = [p for p in Cart.objects.all() if p.user == request.user]

        if cart_product:
            for p in cart_product:
                tempamount = p.quantity * p.product.discounted_price
                amount += tempamount

            totalamount = amount + shipping_amount
            return render(request, 'app/addtocart.html', {'carts': cart, 'totalamount': totalamount, 'amount': amount})
        else:
            return render(request, 'app/emtycart.html')

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
            tempamount = p.quantity * p.product.discounted_price
            amount += tempamount
            data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)
# -------------------EndplusCart----------------------


# -----------------------startminuscart------------------
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
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
# ---------------------Endminus------------------------------------------

# ------------------------------removecart----------------------------------
    
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
       
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]

        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
           
        data = {
            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)
# ----------------------------removecart--------------------------------------


                
def buy_now(request):
 return render(request, 'app/buynow.html')

@login_required
def address(request):
 add = Customer.objects.filter(user=request.user)
 return render(request, 'app/address.html',{'add':add,'active': 'btn-primary'})

@login_required
def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html', {'order_placed': op})

# def payment_done(request):
#     user = request.user
#     custid = request.GET.get('custid')
#     customer_obj = Customer.objects.get(id=custid)
#     cart = Cart.objects.filter(user=user)
#     for c in cart:
#         OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
#         c.delete()
#     return redirect("orders")


@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')

    try:
        customer = Customer.objects.get(id=custid)
    except Customer.DoesNotExist:
        # Handle the case where the customer does not exist
        # For example, you could redirect the user to an error page or return an error message.
        return HttpResponse("Customer not found", status=404)

    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()

    return redirect("orders")


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulation!! Registration successfully')
            form.save()
        return render(request, 'app/customerregistration.html', {'form': form})
    
@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    totalamount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        totalamount = amount + shipping_amount

    return render(request, 'app/checkout.html', {'add': add, 'totalamount': totalamount, 'cart_items': cart_items})

# -----------------------------
@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})

    def post(self, request):  # Corrected the method signature
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']  # Corrected 'cleaned_date' to 'cleaned_data'
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']  # Corrected 'stste' to 'state'
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr, name=name, locality=locality, city=city, state=state, zipcode=zipcode) 
            reg.save()

            messages.success(request,'Congratulations!! Profile Updated Successfully')  # Corrected 'Messages' to 'messages'
            return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})

   