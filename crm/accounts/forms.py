from django.forms import ModelForm
from .models import Order, Customer, Product

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 

from django.contrib.auth.models import User 

from django.forms.widgets import PasswordInput, TextInput

from django import forms



class UserRegisterForm(UserCreationForm):

    class Meta:

        model = User
        fields = ['username', 'email','password1', 'password2' ]

class LoginForm(AuthenticationForm):

    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())


class CreateOrderForm(ModelForm):

    class Meta:

        model = Order
        fields = ['customer', 'product', 'status']

class UpdateOrderForm(ModelForm):

    class Meta:

        model = Order
        fields = ['customer', 'product', 'status']


class CreateCustomerForm(ModelForm):

    class Meta:

        model = Customer
        fields = ['name', 'phone', 'email','profile_pic']

class UpdateCustomerForm(ModelForm):

    class Meta:

        model = Customer
        fields = ['name', 'phone', 'email']


class CreateProductForm(ModelForm):

    class Meta:

        model = Product
        fields = ['name', 'price', 'category', 'description', 'tag']
