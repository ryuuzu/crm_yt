"""crm_yt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from .views import *


app_name = 'accounts'
urlpatterns = [
    path('login/', login, name="login"),
    path('register/', register, name="register"),
    path('logout/', logout, name="logout"),

    path('', home, name='dashboard'),
    path('user/', user, name='user'),
    path('customer/<int:pk>/', customer, name='customer'),
    path('products/', products, name='products'),
    path('customer/create_order/<int:pk>',
         customer_create_order, name="customer_create_order"),
    path('create_order/', create_order, name="create_order"),
    path('update_order/<int:pk>', update_order, name="update_order"),
    path('delete_order/<int:pk>', delete_order, name="delete_order"),
]
