from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.contrib import messages
from django.contrib.auth import authenticate, login as lgin, logout as lgout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User

from .decorators import admin_only, allowed_users, unauthenticated_user
from .models import *
from .forms import OrderForm, CreateUserForm
from .filters import OrderFilter


@unauthenticated_user
def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            lgin(request, user)
            return redirect('accounts:dashboard')
        else:
            messages.info(request, "Username/Password is incorrect")

    context = {}
    return render(request, "accounts/login.html", context)


@unauthenticated_user
def register(request):

    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user: User = form.save()
            group = Group.objects.get(name="Customer")

            user.groups.add(group)
            Customer.objects.create(user=user, name=user.username)

            username = form.cleaned_data.get('username')
            messages.success(request, f"Account was created for {username}")
            return redirect("accounts:login")

    context = {'form': form}
    return render(request, "accounts/register.html", context)


@login_required(login_url="accounts:login")
@allowed_users(allowed_roles=['Customer'])
def user(request: HttpRequest):
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    total_delivered = orders.filter(status="Delivered").count()
    total_pending = orders.filter(status="Pending").count()

    context = {'orders': orders,
               'total_orders': total_orders,
               'total_delivered': total_delivered, 'total_pending': total_pending}
    return render(request, "accounts/user.html", context)


@login_required(login_url='accounts:login')
@admin_only()
def home(request):
    context = {'page_name': 'Dashboard',
               'customers': Customer.objects.all(), 'orders': Order.objects.all(),
               'total_customers': Customer.objects.all().count(),
               'total_orders': Order.objects.all().count(),
               'total_delivered': Order.objects.filter(status='Delivered').count(),
               'total_pending': Order.objects.filter(status='Pending').count(), }
    return render(request, 'accounts/dashboard.html', context=context)


@login_required(login_url='accounts:login')
def logout(request):
    lgout(request)
    return redirect("accounts:login")


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['Admin'])
def products(request):
    products = Product.objects.all()
    context = {'page_name': 'Products', "products": products}
    return render(request, 'accounts/products.html', context=context)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['Admin'])
def customer(request, pk):
    customer = Customer.objects.get(id=pk)

    orders = customer.order_set.all()
    totalOrders = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {'page_name': customer.name,
               'customer': customer,
               'orders': orders,
               "filter": myFilter,
               'total_orders': totalOrders}
    return render(request, 'accounts/customer.html', context=context)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['Admin'])
def customer_create_order(request, pk):
    OrderFormSet = inlineformset_factory(
        Customer, Order, fields=('product', 'status', 'note'), extra=5)
    customer = Customer.objects.get(id=pk)
    formSet = OrderFormSet(instance=customer, queryset=Order.objects.none())

    if request.method == "POST":
        formSet = OrderFormSet(request.POST, instance=customer)
        if formSet.is_valid():
            formSet.save()
            return redirect('accounts:customer', pk=customer.id, permanent=True)

    context = {'page_name': f"{customer.name} - New Order", 'formSet': formSet}
    return render(request, 'accounts/customer_order_form.html', context)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['Admin'])
def create_order(request):
    form = OrderForm()

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'page_name': "New Order", 'form': form}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['Admin'])
def update_order(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'page_name': "New Order", 'form': form}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['Admin'])
def delete_order(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/')
    context = {'order': order}
    return render(request, 'accounts/delete_form.html', context)
