
from django.shortcuts import render, redirect
from .models import Customer, Provider
from car_app.models import Car
import bcrypt
from django.contrib import messages

def dashboard(request):
    return render(request,"dashboard.html")


def search(request):

    if "customer_id" in request.session:
        return redirect("/my_dashboard/search_result")

    return redirect("/search_result")


def search_result(request):

    context = {
        'searched_cars': Provider.objects.filter(location=request.POST["location"])
    }

    return render(request,"search_result.html", context)


def car_select(request, car_id):

    if "customer_id" in request.session:
        return redirect("/my_dashboard/car_details/"+car_id)

    return redirect("/car_details/"+car_id)


def car_details(request, car_id):
    context = {
        'selected_car': Car.objects.get(id=car_id)
    }
    return render(request,"car_details.html", context)


def car_book(request, car_id):
    if "customer_id" in request.session:
        return redirect("/my_dashboard/payment_confirmation/"+car_id)
    return redirect("/register")


def login(request):
    print("this is customer name")
    customer = Customer.objects.filter(email=request.POST["email"])
    if customer:
        errors = Customer.objects.customer_login_validator(request.POST)
        if len(errors) > 0:
            for key, val in errors.items():
                messages.error(request, val)
            return redirect("/")

        logged_customer = customer[0]
        if bcrypt.checkpw(
            request.POST["password"].encode(), logged_customer.password.encode()
        ):
            request.session["customer_id"] = logged_customer.id
            request.session["customer_first_name"] = logged_customer.first_name
        print("this is customer name", request.session["customer_first_name"])
        return redirect("/my_dashboard")

    provider = Provider.objects.filter(email=request.POST["email"])
    if provider:
        errors = Provider.objects.provider_login_validator(request.POST)
        if len(errors) > 0:
            for key, val in errors.items():
                messages.error(request, val)
            return redirect("/")

        logged_provider = provider[0]
        if bcrypt.checkpw(
            request.POST["password"].encode(), logged_provider.password.encode()
        ):
            request.session["provider_id"] = logged_provider.id
            request.session["provider_name"] = logged_provider.name

        return redirect("/my_dashboard/provider_dashboard")


def register(request):
    return render(request,"register.html")

def customer_register(request):

    errors = Customer.objects.customer_validator(request.POST)
    if len(errors) > 0:
        for key, val in errors.items():
            messages.error(request, val)
        return redirect("/register/")

    password = request.POST["password"]
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    Customer.objects.create(
        first_name=request.POST["firstName"],
        last_name=request.POST["lastName"],
        email=request.POST["email"],
        password=pw_hash,
        mobile=request.POST["mobile"],
        birthday=request.POST["birthday"],
        national_id=request.POST["national_id"],
    )
    return redirect("/my_dashboard")

def provider_register(request):

    errors = Provider.objects.provider_validator(request.POST)
    if len(errors) > 0:
        for key, val in errors.items():
            messages.error(request, val)
        return redirect("/register/")

    password_from_form = request.POST["password"]
    pw_hash = bcrypt.hashpw(password_from_form.encode(), bcrypt.gensalt()).decode()

    provider = Provider.objects.create(
        name=request.POST["name"],
        email=request.POST["email"],
        password=pw_hash,
        mobile=request.POST["mobile"],
        permit=request.POST["permit"],
        location=request.POST["location"],
    )
    request.session['provider_id']=provider.id
    request.session['provider_name']=provider.name
    return redirect("/my_dashboard/provider_dashboard")


def delete(request):
    print("logout works")
    if "customer_id" in request.session:

        del request.session["customer_id"]
        del request.session["customer_first_name"]

        return redirect("/")

    if "provider_id" in request.session:
    
        del request.session["provider_id"]
        del request.session["provider_name"]

        return redirect("/")

    else:
        return redirect("/")


def contact(request):
    return render(request, 'contact.html')




