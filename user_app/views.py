from django.shortcuts import render, redirect
from .models import Customer, Provider
from car_app.models import Car
import bcrypt
from django.contrib import messages


def dashboard(request):
    context = {
        "all_providers": Provider.objects.all(),
    }
    return render(request, "dashboard.html", context)


def search(request):

    if "customer_id" in request.session:
        return redirect("/my_dashboard/search_result")

    return redirect("/search_result")


def search_result(request):
    context = {
        "location_filter_provider": Provider.objects.filter(
            location=request.POST["location"]
        ),
    }
    provider = Provider.objects.filter(location=request.POST["location"])
    print(provider)
    return render(request, "search_result.html", context)


def car_select(request):
    # TODO: hidden input is going and car id
    return render(request, "car_details.html")


def car_details(request):
    # TODO: car id is coming as hidden, user is coming as session, need to add them to make booking
    context = {
        # coming from hidden input
        "selected_car": Car.objects.get(id=request.POST["car_id"]),
        "selected_customer": Customer.objects.get(id=request.session["customer_id"]),
    }
    return render(request, "car_details.html", context)


def car_book(request, car_id):
    if "customer_id" in request.session:
        return redirect("/my_dashboard/payment_confirmation/")
    return redirect("/register")


def login(request):

    errors = Provider.objects.provider_login_validator(request.POST)
    if len(errors) > 0:
        for key, val in errors.items():
            messages.error(request, val)
        return redirect("/")
    print("you are here")
    provider = Provider.objects.filter(email=request.POST["email"])
    if provider:
        if bcrypt.checkpw(
            request.POST["password"].encode(), provider[0].password.encode()
        ):
            request.session["provider_id"] = provider[0].id
            request.session["provider_name"] = provider[0].name
            request.session["sign_out"] = "Sign Out"
        return redirect("/my_dashboard/provider_dashboard/")

    customer = Customer.objects.filter(email=request.POST["email"])
    errors = Customer.objects.customer_login_validator(request.POST)
    if len(errors) > 0:
        for key, val in errors.items():
            messages.error(request, val)
        return redirect("/")

    if customer:
        if bcrypt.checkpw(
            request.POST["password"].encode(), customer[0].password.encode()
        ):
            request.session["customer_id"] = customer[0].id
            request.session["customer_first_name"] = customer[0].first_name
            request.session["sign_out"] = "Sign Out"
        return redirect("/")


def register(request):
    return render(request, "register.html")


def customer_register(request):

    errors = Customer.objects.customer_validator(request.POST)
    if len(errors) > 0:
        for key, val in errors.items():
            messages.error(request, val)
        return redirect("/register/")

    password = request.POST["password"]
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    customer = Customer.objects.create(
        first_name=request.POST["firstName"],
        last_name=request.POST["lastName"],
        email=request.POST["email"],
        password=pw_hash,
        mobile=request.POST["mobile"],
        birthday=request.POST["birthday"],
        # national_id=request.POST["national_id"],
    )
    request.session["customer_id"] = customer.id
    request.session["customer_first_name"] = customer.first_name
    request.session["sign_out"] = "Sign Out"
    return redirect("/")


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
        # permit=request.POST["permit"],
        location=request.POST["location"],
    )
    request.session["provider_id"] = provider.id
    request.session["provider_name"] = provider.name
    request.session["sign_out"] = "Sign Out"

    return redirect("/my_dashboard/provider_dashboard")


def delete(request):

    if "customer_id" in request.session:
        del request.session["customer_id"]
        del request.session["customer_first_name"]
        del request.session["sign_out"]

        return redirect("/")

    if "provider_id" in request.session:

        del request.session["provider_id"]
        del request.session["provider_name"]
        del request.session["sign_out"]

        return redirect("/")


def contact(request):
    return render(request, "contact.html")
