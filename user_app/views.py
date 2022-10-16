
from django.shortcuts import render, redirect
from .models import Customer, Provider, Website_review
from django.http import JsonResponse
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

    pick_up_date = request.POST["pick_up_date"]
    drop_off_date = request.POST["drop_off_date"]
    request.session["pick_up_date"] = pick_up_date
    request.session["drop_off_date"] = drop_off_date
    print("tyhis works here", pick_up_date)

    return redirect("/search_result")


def search_result(request):

    context = {
        "searched_cars": Provider.objects.filter(location=request.POST["location"])
    }

    return render(request, "search_result.html", context)


def car_select(request, car_id):

    if "customer_id" in request.session:
        return redirect("/my_dashboard/car_details/" + car_id)

    return redirect("/car_details/" + car_id)


def car_details(request, car_id):
    context = {"selected_car": Car.objects.get(id=car_id)}
    return render(request, "car_details.html", context)


def car_book(request, car_id):
    if "customer_id" in request.session:
        return redirect("/my_dashboard/payment_confirmation/" + car_id)
    return redirect("/register")


def login(request):

    customer = Customer.objects.filter(email=request.POST["email"])
    if customer:
        errors = Customer.objects.customer_login_validator(request.POST)
        if len(errors) > 0:
            for key, val in errors.items():
                messages.error(request, val)
            return redirect("/")

        logged_customer = customer[0]
        if bcrypt.checkpw(
            request.POST["password"].encode(
            ), logged_customer.password.encode()
        ):
            request.session["customer_id"] = logged_customer.id
            request.session["customer_first_name"] = logged_customer.first_name
            request.session["sign_out"] = "Sign Out"
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
            request.POST["password"].encode(
            ), logged_provider.password.encode()
        ):
            request.session["provider_id"] = logged_provider.id
            request.session["provider_name"] = logged_provider.name
            request.session["sign_out"] = "Sign Out"

        return redirect("/my_dashboard/provider_dashboard")
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
        profile=request.FILES["profile"],
        first_name=request.POST["firstName"],
        last_name=request.POST["lastName"],
        email=request.POST["email"],
        password=pw_hash,
        mobile=request.POST["mobile"],
        birthday=request.POST["birthday"],
        driving_license=request.FILES["driving_license"],
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
    pw_hash = bcrypt.hashpw(password_from_form.encode(),
        bcrypt.gensalt()).decode()

    provider = Provider.objects.create(
        name=request.POST["name"],
        email=request.POST["email"],
        password=pw_hash,
        mobile=request.POST["mobile"],
        permit=request.FILES["permit"],
        logo=request.FILES["logo"],
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


def delete_account(request):

    if "customer_id" in request.session:
        c = Customer.objects.get(id=request.session["customer_id"])
        c.delete()
        del request.session["customer_id"]
        del request.session["customer_first_name"]
        del request.session["sign_out"]

        return redirect("/")

    if "provider_id" in request.session:
        c = Provider.objects.get(id=request.session["provider_id"])
        c.delete()
        del request.session["provider_id"]
        del request.session["provider_name"]
        del request.session["sign_out"]

        return redirect("/")


def contact(request):
    return render(request, "contact.html")


def website_review(request):
    review = Website_review.objects.create(
        first_name=request.POST["first_name"],
        last_name=request.POST["last_name"],
        email=request.POST["email"],
        message=request.POST["message"],
    )
    if review.id:
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


def check_email(request, email=""):
    customer = Customer.objects.filter(email=email)
    if customer:
        return JsonResponse({"exists": True})
    return JsonResponse({"exists": False})

def check_email_provider(request, email=""):
    provider = Provider.objects.filter(email=email)
    if provider:
        return JsonResponse({"exists": True})
    return JsonResponse({"exists": False})
