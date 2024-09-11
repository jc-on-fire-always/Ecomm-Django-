from django.shortcuts import render,redirect
from django.db.models import Count
from django.http import HttpResponse,JsonResponse
from urllib import request
from django.views import View
import razorpay
from . models import Product,Customer,Cart,Payment,OrderPlaced,Wishlist
from . forms import CustomerRegistrationForm,CustomerLoginForm,CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


@login_required
def home(request):
  totalitem = 0
  totalitemWishlist =  0
  if request.user.is_authenticated:
    totalitem = len(Cart.objects.filter(user=request.user))
    totalitemWishlist= len(Wishlist.objects.filter(user=request.user))
  return render(request,"app/home.html")

def about(request):
  totalitem = 0
  totalitemWishlist = 0
  if request.user.is_authenticated:
     totalitem = len(Cart.objects.filter(user=request.user))
     totalitemWishlist = len(Wishlist.objects.filter(user=request.user))
  return render(request,"app/about.html",locals())

def contact(request):
  totalitem = 0
  totalitemWishlist =  0
  if request.user.is_authenticated:
    totalitem = len(Cart.objects.filter(user=request.user))
    totalitemWishlist= len(Wishlist.objects.filter(user=request.user))
  return render(request,"app/contact.html",locals())


@method_decorator(login_required,name='dispatch')
class CategoryView(View):
  def get(self,request,val):
    totalitem = 0
    totalitemWishlist =  0
    if request.user.is_authenticated:
      totalitem = len(Cart.objects.filter(user=request.user))
      totalitemWishlist= len(Wishlist.objects.filter(user=request.user))
    product = Product.objects.filter(category=val)
    title = Product.objects.filter(category=val).values('title')
    return render(request,"app/category.html",locals())
  
class CategoryTitle(View):
  def get(self,request,val):
    totalitem = 0
    totalitemWishlist =  0
    if request.user.is_authenticated:
      totalitem = len(Cart.objects.filter(user=request.user))
      totalitemWishlist= len(Wishlist.objects.filter(user=request.user))
    product = Product.objects.filter(title=val)
    title = Product.objects.filter(category=product[0].category).values('title')
    return render(request,"app/category.html",locals())
  

class ProductDetail(View):
  def get(self,request,pk):
    totalitem = 0
    totalitemWishlist =  0
    if request.user.is_authenticated:
      totalitem = len(Cart.objects.filter(user=request.user))
      totalitemWishlist= len(Wishlist.objects.filter(user=request.user))
    product = Product.objects.get(pk=pk)
    if request.user.is_authenticated:
        wishlist = Wishlist.objects.filter(user=request.user, product=product).exists()
    else:
        wishlist = False
    return render(request,"app/product-detail.html",locals())
  

class CustomerRegistrationView(View):
  def get(self,request):
    totalitem = 0
    totalitemWishlist =  0
    if request.user.is_authenticated:
      totalitem = len(Cart.objects.filter(user=request.user))
      totalitemWishlist= len(Wishlist.objects.filter(user=request.user))
    form = CustomerRegistrationForm()
    return render(request,"app/customer-register.html",locals())
  def post(self,request):
    form = CustomerRegistrationForm(request.POST)
    if(form.is_valid()):
      form.save()
      messages.success(request,"User Registered Successfully!")
    else:
      messages.warning(request,"Invalid Input Data")
    return render(request,"app/customer-register.html",locals())
  
class CustomerLoginView(View):
  def get(self,request):
    totalitem = 0
    totalitemWishlist =  0
    if request.user.is_authenticated:
      totalitem = len(Cart.objects.filter(user=request.user))
      totalitemWishlist= len(Wishlist.objects.filter(user=request.user))
    form = CustomerLoginForm()
    return render(request,"app/customer-login.html",locals())
  def post(self,request):
    form = CustomerLoginForm(request.POST)
    if(form.is_valid()):
      form.save()
      #messages.success(request,"Logged In")
    else:
      messages.warning(request,"Invalid Input Data")
    return render(request,"app/home.html",locals())
  
class ProfileView(View):
  def get(self,request):
    totalitem = 0
    totalitemWishlist =  0
    if request.user.is_authenticated:
      totalitem = len(Cart.objects.filter(user=request.user))
      totalitemWishlist= len(Wishlist.objects.filter(user=request.user))  
    form = CustomerProfileForm()
    return render(request,"app/profile.html",locals())
  def post(self,request):
    form = CustomerProfileForm(request.POST)
    if form.is_valid():
      user = request.user
      name = form.cleaned_data['name']
      locality = form.cleaned_data['locality']
      city = form.cleaned_data['city']
      mobile = form.cleaned_data['mobile']
      state = form.cleaned_data['state']
      zipcode = form.cleaned_data['zipcode']

      reg = Customer(user=user,name=name,locality=locality,city=city,mobile=mobile,state=state,zipcode=zipcode)
      reg.save()
      messages.success(request,"Profile Saved Successfully")
    else:
      messages.warning(request,"Invalid Input Data")
    return render(request,"app/profile.html",locals())
  
def address(request):
  totalitem = 0
  totalitemWishlist =  0
  if request.user.is_authenticated:
    totalitem = len(Cart.objects.filter(user=request.user))
    totalitemWishlist= len(Wishlist.objects.filter(user=request.user))
  add = Customer.objects.filter(user=request.user)
  return render(request,"app/address.html",locals())


class UpdateAddress(View):
  def get(self,request,pk):
    totalitem = 0
    totalitemWishlist =  0
    if request.user.is_authenticated:
      totalitem = len(Cart.objects.filter(user=request.user))
      totalitemWishlist= len(Wishlist.objects.filter(user=request.user))
    add = Customer.objects.get(pk=pk)
    form = CustomerProfileForm(instance=add)
    return render(request,"app/updateAddress.html",locals())
  def post(self,request,pk):
    form = CustomerProfileForm(request.POST)
    if form.is_valid():
      add = Customer.objects.get(pk=pk)
      add.name = form.cleaned_data['name']
      add.locality = form.cleaned_data['locality']
      add.city = form.cleaned_data['city']
      add.mobile = form.cleaned_data['mobile']
      add.state = form.cleaned_data['state']
      add.zipcode = form.cleaned_data['zipcode']
      add.save()
      messages.success(request, "Congratulations! Profile Updated Successfully")
    else:
      messages.warning (request, "Invalid Input Data")
    return redirect("address")



def add_to_cart(request):
  user=request.user
  product_id=request.GET.get('prod_id')
  product=Product.objects.get(id=product_id)
  Cart(user=user,product=product).save();
  return redirect("/cart")

def show_cart(request):
  totalitem = 0
  totalitemWishlist =  0
  if request.user.is_authenticated:
    totalitem = len(Cart.objects.filter(user=request.user))
    totalitemWishlist= len(Wishlist.objects.filter(user=request.user))  
  user=request.user
  cart = Cart.objects.filter(user=user)
  amount = 0
  for p in cart:
      value = p.quantity * p.product.discounted_price
      amount = amount + value
  totalamount = amount + 40

  return render(request,"app/addToCart.html",locals())


def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = (amount + 40 if amount > 0 else 0)
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)

def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = (amount + 40 if amount > 0 else 0)
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)
    
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = (amount + 40 if amount > 0 else 0)
        data = {
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)


class checkout(View):
  def get(self, request):
    totalitem = 0
    totalitemWishlist =  0
    if request.user.is_authenticated:
      totalitem = len(Cart.objects.filter(user=request.user))
      totalitemWishlist= len(Wishlist.objects.filter(user=request.user))
    user=request.user
    add=Customer.objects.filter(user=user)
    cart_items=Cart.objects.filter(user=user)
    famount = 0
    for p in cart_items:
      value = p.quantity * p.product.discounted_price
      famount = famount + value
    totalamount = famount + 40
    razoramount = int(totalamount * 100)
    client = razorpay.Client(auth=(settings.RAZOR_KEY_ID,settings.RAZOR_KEY_SECRET))
    data = {"amount": razoramount,"currency":"INR","receipt":"order_rcptid_11"}
    payment_response = client.order.create(data=data)
    print(payment_response)
    order_id = payment_response['id']
    order_status = payment_response['status']
    if order_status == 'created':
        payment = Payment(
            user=user,
            amount=totalamount,
            razorpay_order_id=order_id,
            razorpay_payment_status=order_status
        )
        payment.save()

    return render(request, 'app/checkout.html', locals())
  
def payment_done(request):
    order_id = request.GET.get('order_id')
    payment_id = request.GET.get('payment_id')
    cust_id = request.GET.get('cust_id')
    # print("payment_done : oid = ", order_id, " pid = ", payment_id, " cid = ", cust_id)
    user = request.user
    # return redirect("orders")

    customer = Customer.objects.get(id=cust_id)
    # To update payment status and payment id
    payment = Payment.objects.get(razorpay_order_id=order_id)
    payment.paid = True
    payment.razorpay_payment_id = payment_id
    payment.save()

    # To save order details
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity, payment=payment).save()
        c.delete()

    return redirect("orders")

def orders(request):
  totalitem = 0
  totalitemWishlist =  0
  if request.user.is_authenticated:
    totalitem = len(Cart.objects.filter(user=request.user))
    totalitemWishlist= len(Wishlist.objects.filter(user=request.user))
  order_placed = OrderPlaced.objects.filter(user=request.user)
  return render(request,'app/orders.html',locals())


def plus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        user = request.user
        Wishlist(user=user, product=product).save()
        data = {
            'message': 'Wishlist Added Successfully',
        }
        return JsonResponse(data)

def minus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        user = request.user
        Wishlist.objects.filter(user=user, product=product).delete()
        data = {
            'message': 'Wishlist Remove Successfully',
        }
        return JsonResponse(data)


def search(request):
  totalitem = 0
  totalitemWishlist =  0
  if request.user.is_authenticated:
    totalitem = len(Cart.objects.filter(user=request.user))
    totalitemWishlist= len(Wishlist.objects.filter(user=request.user))
    
  query = request.GET["search"]
  product = Product.objects.filter(Q(title__icontains=query))
  return render(request,"app/search.html",locals())



def show_wishlist(request):
    user = request.user
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    product = Wishlist.objects.filter(user=user)
    return render(request, "app/wishlist.html", locals())

    


