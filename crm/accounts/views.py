from django.shortcuts import render, redirect
from django.http import HttpResponse
from . models import (Customer, Product,Order )
from .forms import (CreateOrderForm, 
                    UpdateOrderForm, 
                    CreateCustomerForm,
                    UpdateCustomerForm,
                    CreateProductForm,
                    UserRegisterForm,
                    LoginForm,
                    )

from django.forms import inlineformset_factory

from django.contrib.auth import authenticate

from django.contrib.auth.models import auth

from django.contrib import messages

from django.contrib.auth.decorators import login_required

from .decorators import unauthenticated_user, allowed_users, admin_only

from . filters import OrderFilter

from django.contrib.auth.models import Group




# Create your views here.

@login_required(login_url='my-login')
@admin_only
def Home(request):

    return render(request, 'acc/index.html')

@unauthenticated_user
def Register(request):

    form = UserRegisterForm()

    if request.method == 'POST':

        form = UserRegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            group = Group.objects.get(name='customer')
            user.groups.add(group)
            Customer.objects.create(
                user=user,
            )

            username = form.cleaned_data.get('username')
            messages.success(request, 'Sucessfully ' +  username  + ' Registred!')

            return redirect('my-login')
        
    context = {'form':form}

    return render(request, 'acc/register.html', context)

@unauthenticated_user
def Login(request):

    form = LoginForm()

    if request.method == 'POST': 

        form = LoginForm(request, data=request.POST)

        if form.is_valid():

            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(request, username=username, password=password)

            if user is not None:

                auth.login(request, user)
                
                messages.success(request, 'Sucessfully Login!')

                return redirect('my-home')

    context = {'form':form}

    return render(request, 'acc/login.html', context)


@login_required(login_url='my-login')
@allowed_users(allowed_roles=['customer'])
def Settings(request):

    customer = request.user.customer
    form = CreateCustomerForm(instance=customer)

    if request.method == 'POST':
         form = CreateCustomerForm(request.POST, request.FILES, instance=customer)
         if form.is_valid():
             form.save()

    context = {'form':form}
    return render(request, 'acc/settings.html', context)

@login_required(login_url='my-login')

def Logout(request):

    auth.logout(request)

    messages.success(request, 'Sucessfully Logged out!')

    return redirect("my-home")

@login_required(login_url='my-login')
@allowed_users(allowed_roles=['customer'])
def UserPage(request):
    orders = request.user.customer.order_set.all()

    total_order = orders.count()

    order_pending = orders.filter(status= 'Pending').count()

    order_delivered = orders.filter(status= 'Delivered').count()

    context = {'orders':orders,
                'total_order':total_order,
                'order_pending':order_pending,
                'order_delivered':order_delivered,
                }
    return render(request, 'acc/user.html', context)


@login_required(login_url='my-login')
@allowed_users(allowed_roles=['admin'])
def Dashboard(request):

    customer = Customer.objects.all().order_by('-id')

    order = Order.objects.all().order_by('-id')

    total_order = order.count()

    order_pending = order.filter(status= 'Pending').count()

    order_delivered = order.filter(status= 'Delivered').count()

    context = {'customer':customer,
                'order':order,
                'total_order':total_order,
                'order_pending':order_pending,
                'order_delivered':order_delivered,
              }

    return render(request, 'acc/dashboard.html', context)

@login_required(login_url='my-login')
@allowed_users(allowed_roles=['admin'])
def Products(request):

    products = Product.objects.all().order_by('-id')

    context = {'product': products}

    return  render(request, 'acc/products.html',context)


@login_required(login_url='my-login')
@allowed_users(allowed_roles=['admin'])
def AddProducts(request):

    form = CreateProductForm()

    if request.method == 'POST':

        form = CreateProductForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(request, 'Sucessfully Product added!')

            return redirect('my-products')
        
    context = {'form':form}

    return render(request, 'acc/add_products.html', context)

@login_required(login_url='my-login')
@allowed_users(allowed_roles=['admin'])
def Customers(request, pk):

    customer = Customer.objects.get(id=pk)
    
    order = customer.order_set.all()

    my_filter = OrderFilter(request.GET, queryset=order)
    order = my_filter.qs

    total_order = order.count()

    context = { 'customer':customer,
                'order':order, 
                'total_order':total_order,
                'my_filter':my_filter,
                }
   
    return  render(request, 'acc/customer.html', context)


@login_required(login_url='my-login')
@allowed_users(allowed_roles=['admin'])
def CreateCustomer(request):

    form = CreateCustomerForm()

    if request.method == 'POST':

        form = CreateCustomerForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(request, 'Sucessfully Customer Created!')

            return redirect('my-dashboard')
        
    context = {'form':form}

    return render(request, 'acc/create_customer.html', context)


@login_required(login_url='my-login')
@allowed_users(allowed_roles=['admin'])
def Updatecustomer(request, pk):

    customer = Customer.objects.get(id=pk)

    form = UpdateCustomerForm(instance=customer)

    if request.method == 'POST':

        form = UpdateCustomerForm(request.POST, instance=customer)

        if form.is_valid():

            form.save()

            messages.success(request, 'Sucessfully Customer Updated')

            return redirect('my-dashboard')
        
    context = {'form':form, 'customer':customer}

    return render(request, 'acc/update_customer.html', context)


@login_required(login_url='my-login')
@allowed_users(allowed_roles=['admin'])
def CreateOrders(request, pk):

    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10)

    customer = Customer.objects.get(id=pk)

    # form = CreateOrderForm(initial={'customer':customer})

    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)

    if request.method == 'POST':

        # form = CreateOrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)

        if formset.is_valid():

            formset.save()

            messages.success(request, 'Sucessfully Order Created!')


            return redirect('my-dashboard')
       
    context = {'formset':formset, 'customer':customer}

    return render(request, 'acc/order_form.html', context)



@login_required(login_url='my-login')
@allowed_users(allowed_roles=['admin'])
def UpdateOrder(request, pk):

    order = Order.objects.get(id=pk)

    form = UpdateOrderForm(instance=order)

    if request.method == "POST":

        form = UpdateOrderForm(request.POST ,instance=order)

        if form.is_valid():

            form.save()

            messages.success(request, 'Sucessfully Order Updated!')

            return redirect('my-dashboard')
       
    context = {'form':form}

    return render(request, 'acc/update_order.html',context)


@login_required(login_url='my-login')
@allowed_users(allowed_roles=['admin'])
def DeleteOrder(request, pk):

    order = Order.objects.get(id=pk)

    if request.method == "POST":

        order.delete()

        messages.success(request, 'Sucessfully Order Deleted!')

        return redirect('my-dashboard')
    
    context = {'item':order} 
    
    return render(request, 'acc/delete_order.html', context)



   

  


