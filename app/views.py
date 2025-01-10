from django.shortcuts import render, redirect
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced
from .forms import CustomerRegistrationForm, CustomerprofileForm
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.db.models import Q
from django.http import JsonResponse
def home(request):
 return render(request, 'app/home.html')

class ProductView(View):
    def get(self, request):
        if 'q' in request.GET:
            q = request.GET.get('q', '')  # Get the search query or an empty string if not provided
            # Assuming Product has a 'user' field
            all_products = Product.objects.filter(title__icontains=q)
            return render(request, "app/search_results.html", {'product': all_products, 'query': q})

        totalitem = 0
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')
        if request.user.is_authenticated:
           wwe = len(Cart.objects.filter(user=request.user))
           return render(request, 'app/home.html', {'topwears':topwears, 'bottomwears':bottomwears,
           'mobiles':mobiles, 'totalitem':wwe}) 

        return render(request, 'app/home.html', {'topwears':topwears, 'bottomwears':bottomwears,
         'mobiles':mobiles}) 


 
class ProductDetailView(View):
    def get(self, request ,pk):
        product = Product.objects.get(pk=pk)
        return render(request, 'app/productdetail.html', {'product':product })

def add_to_cart(request):
 user = request.user
 product_id = request.GET.get('prod_id')
 product = Product.objects.get(id=product_id)
 Cart(user=user, product=product).save()
 return redirect('/cart')

def show_cart(request):
    if request.user.is_authenticated:
       user = request.user
       cart = Cart.objects.filter(user=user)
       amount = 0.0
       shipping_amount = 70.0
       total_amount = 0.0
       cart_prouduct = [p for p in Cart.objects.all() if p.user == user]
       if cart_prouduct:
          for p in cart:
             tempamount = (p.quantity * p.product.discounted_price)
             amount += tempamount
             totalamount = amount + shipping_amount
          return render(request, 'app/addtocart.html', {'carts':cart, 'totalamount':totalamount, 'amount':amount })
       else:
          return render(request, 'app/emptycart.html')  

def plus_cart(request):
   if request.method == "GET":
      prod_id  = request.GET['prod_id']
      c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
      c.quantity+=1
      c.save()
      amount = 0.0
      shipping_amount = 70.0
      cart_prouduct = [p for p in Cart.objects.all() if p.user == request.user]
      for p in cart_prouduct:
             tempamount = (p.quantity * p.product.discounted_price)
             amount += tempamount
             totalamount = amount + shipping_amount
      data = {
            'quantity': c.quantity,
            'amount' :amount,
            'totalamount':totalamount
            }
      return JsonResponse(data)

def minus_cart(request):
   if request.method == "GET":
      prod_id  = request.GET['prod_id']
      c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
      c.quantity-=1
      c.save()
      amount = 0.0
      shipping_amount = 70.0
      cart_prouduct = [p for p in Cart.objects.all() if p.user == request.user]
      for p in cart_prouduct:
             tempamount = (p.quantity * p.product.discounted_price)
             amount += tempamount
             totalamount = amount + shipping_amount
      data = {
            'quantity': c.quantity,
            'amount' :amount,
            'totalamount':totalamount
            }
      return JsonResponse(data)

def remove_cart(request):
   if request.method == "GET":
      prod_id  = request.GET['prod_id']
      c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
      c.delete()
      amount = 0.0
      shipping_amount = 70.0
      cart_prouduct = [p for p in Cart.objects.all() if p.user == request.user]
      for p in cart_prouduct:
             tempamount = (p.quantity * p.product.discounted_price)
             amount += tempamount
      data = {
            'amount' :amount,
            'totalamount':amount + shipping_amount
            }
      return JsonResponse(data)






def buy_now(request):
 return render(request, 'app/buynow.html')




def address(request):
 add = Customer.objects.filter(user=request.user)
 return render(request, 'app/address.html', {'add':add, 'active':'btn-primary'})

def orders(request):
 return render(request, 'app/orders.html')

def change_password(request):
 return render(request, 'app/changepassword.html')

def mobile(request, data=None):
    if data == None:
       mobile = Product.objects.filter(category='M')
    elif data == 'Rog' or data == 'xiaomi' or data == 'oneplus':
       mobile = Product.objects.filter(category='M').filter(brand=data)
    return render(request, 'app/mobile.html', {'mobiles':mobile})


def topwear(request):
   topwear = Product.objects.filter(category='BW')
   return render(request, 'app/topwear.html', {'topwear':topwear})

def bottomwear(request):
   bottomwear = Product.objects.filter(category='TW')
   return render(request, 'app/bottomwear.html', {'bottomwear':bottomwear})




def logout_view(request):
    logout(request)
    return redirect('login')

def login(request):
 return render(request, 'app/login.html')

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form':form})
    def post(self, request):
      form = CustomerRegistrationForm(request.POST)
      if form.is_valid():
        messages.success(request, 'Congraglations you Registred!!')
        form.save()
      return render(request, 'app/customerregistration.html', {'form':form})



def checkout(request):
   user = request.user
   add = Customer.objects.filter(user=user)
   cart_items = Cart.objects.filter(user=user)
   amount = 0.0
   shipping_amount = 70.0
   cart_prouduct = [p for p in Cart.objects.all() if p.user == request.user]
   for p in cart_prouduct:
         tempamount = (p.quantity * p.product.discounted_price)
         amount += tempamount
         totalamount = amount + shipping_amount
   return render(request, 'app/checkout.html', {'add':add, 'totalamount':totalamount, 'cart_items':cart_items})



class Profile(View):
   def get(self, request):
      form = CustomerprofileForm()
      return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary'})
   def post(self, request):
       form = CustomerprofileForm(request.POST)
       if form.is_valid():
          usr = request.user
          nm = form.cleaned_data['name']
          local = form.cleaned_data['locality']
          ci = form.cleaned_data['city']
          stat = form.cleaned_data['state']
          zip = form.cleaned_data['zipcode']
          reg = Customer(user=usr, name=nm, locality=local, city=ci, state=stat, zipcode=zip)
          reg.save()
          messages.success(request, 'concratulationd!! profile updated Successfully')
       return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary'}) 
