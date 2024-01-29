from django.urls import path
from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [


    path('', views.Home, name='my-home'),
    path('register/', views.Register, name='my-register'),
    path('login/', views.Login, name='my-login'),
    path('logout/', views.Logout, name='my-logout'),
    path('userpage/', views.UserPage, name='my-userpage'),
    path('settings/', views.Settings, name='my-settings'),
    path('dashboard/', views.Dashboard, name='my-dashboard'),
    path('products/', views.Products, name='my-products'),
    path('addproducts/', views.AddProducts, name='my-addproducts'),
    path('customer/<str:pk>', views.Customers, name='my-customer'),
    path('order/<str:pk>', views.CreateOrders, name='my-order'),
    path('updateorder/<str:pk>', views.UpdateOrder, name='my-updateorder'),
    path('deleteorder/<str:pk>', views.DeleteOrder, name='my-deleteorder'),
    path('createcustomer/', views.CreateCustomer, name='my-createcustomer'),
    path('updatecustomer/<str:pk>', views.Updatecustomer, name='my-updatecustomer'),

    path('reset_password', auth_views.PasswordResetView.as_view(), name="reset_password"),

    path('reset_password_sent', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),

    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),

    path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),

]
#template_name="acc/reset_password.html"

#template_name="acc/password_reset_done.html"

 #template_name="acc/password_reset_confirm.html"
 #template_name="acc/password_reset_complete.html"