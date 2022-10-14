from django.shortcuts import render, redirect
from user_app.models import Provider, Customer, Customer_payment, Provider_payment
from .models import Car, Booking
import bcrypt


def my_dashboard(request):

    if "customer_id" not in request.session:
        return redirect("/")

    customer_id = request.session["customer_id"]

    context = {
        "customer_id": customer_id,
        "customer": Customer.objects.get(id=request.session["customer_id"]),
        "all_providers": Provider.objects.all(),
    }
    return render(request, "dashboard.html", context)


def customer_search(request):

    request.session["location"] = request.POST["location"]
    request.session["pick_up_date"] = request.POST["pick_up_date"]
    request.session["drop_off_date"] = request.POST["drop_off_date"]

    return redirect("/my_dashboard/search_result")


def customer_search_result(request):

    context = {
        "searched_cars": Provider.objects.filter(location=request.POST["location"])
    }

    return render(request, "search_result.html", context)


def customer_car_select(request, car_id):
    return redirect("/my_dashboard/car_details/" + car_id)


def customer_car_details(request, car_id):
    context = {
        "selected_car": Car.objects.get(id=car_id),
    }
    return render(request, "car_details.html", context)


def customer_car_book(request, car_id):

    return redirect("/my_dashboard/payment_confirmation/" + car_id)


def provider_dashboard(request):

    context = {
        "provider_cars": Provider.objects.get(
            id=request.session["provider_id"]
        ).cars.all(),
    }
    return render(request, "provider_dashboard.html", context)


def car_book(request, car_id):
    return redirect("/my_dashboard/payment_confirmation/" + car_id)


def payment_confirmation(request, car_id):
    selected_car = Car.objects.get(id=car_id)
    customer_id = request.session["customer_id"]
    context = {
        "car_to_book": selected_car,
        "customer_id": customer_id,
        "customer_cards": Customer.objects.get(id=customer_id)
        .customer_cards.all(),
    }
    # print(selected_car.price)
    return render(request, "payment_confirmation.html", context)


def confirm_book(request, car_id):
    print("this works here lalalalala")
    Booking.objects.create(
        pick_up_date=request.session.get("pick_up_date"),
        drop_off_date=request.session.get("drop_off_date"),
        status="Pending",
        customer_book=Customer.objects.get(id=request.session["customer_id"]),
        car_book=Car.objects.get(id=car_id),
    )

    return redirect("/my_dashboard")


def customer_payment_method(request, customer_id):

    context = {
        "customer": Customer.objects.get(id=customer_id),
        "link": "/my_dashboard/customer_add_payment/" + customer_id + "/",
    }
    return render(request, "payment_method.html", context)


def Provider_payment_method(request, provider_id):

    context = {
        "provider": Provider.objects.get(id=provider_id),
        "link": "/my_dashboard/provider_add_payment/" + provider_id + "/",
    }

    return render(request, "payment_method.html", context)


def add_car(request):
    context = {
        "provider": Provider.objects.get(id=request.session["provider_id"]),
    }
    return render(request, "add_car.html", context)


def insert_car(request):

    Car.objects.create(
        brand=request.POST["brand"],
        model=request.POST["model"],
        color=request.POST["color"],
        production_year=request.POST["production_year"],
        plate_number=request.POST["plate_number"],
        price=request.POST["price"],
        photo=request.FILES["photo"],
        provider=Provider.objects.get(id=request.session["provider_id"]),
    )
    return redirect("/my_dashboard/add_car")


def edit_car(request, car_id):

    context = {
        "garage": Car.objects.filter(provider=request.session["provider_id"]),
        "car_id": car_id,
        "car": Car.objects.get(id=car_id),
    }
    return render(request, "edit_car.html", context)


def edit_my_car(request, car_id):

    print("this works here")

    c = Car.objects.get(id=car_id)
    c.brand = request.POST["brand"]
    c.model = request.POST["model"]
    c.color = request.POST["color"]
    c.production_year = request.POST["production_year"]
    c.plate_number = request.POST["plate_number"]
    c.price = request.POST["price"]
    c.photo = (request.FILES["photo"],)
    c.save()

    return redirect("/my_dashboard/edit_car/" + car_id)


def provider_account(request, provider_id):
    print("this works here")
    context = {
        "provider_id": provider_id,
        "provider": Provider.objects.get(id=provider_id),
        "cards": Provider_payment.objects.filter(provider_payment=provider_id),
    }

    return render(request, "provider_account.html", context)


def provider_account_edit(request, provider_id):

    provider = Provider.objects.filter(name=request.session["provider_name"])
    if provider:
        logged_provider = provider[0]
        if bcrypt.checkpw(
            request.POST["password"].encode(), logged_provider.password.encode()
        ):
            password_from_form = request.POST["new_password"]
            pw_hash = bcrypt.hashpw(
                password_from_form.encode(), bcrypt.gensalt()
            ).decode()

    c = Provider.objects.get(id=provider_id)
    c.name = request.POST["name"]
    c.location = request.POST["location"]
    c.email = request.POST["email"]
    c.password = pw_hash
    c.permit = request.FILES["permit"]
    c.logo = request.FILES["logo"]
    c.mobile = request.POST["mobile"]
    c.save()

    return redirect("/my_dashboard/provider_account/" + provider_id)


def provider_car_details(request, car_id):
    print("thisworks here")
    context = {"selected_car": Car.objects.get(id=car_id)}
    return render(request, "provider_car_details.html", context)


def customer_account(request, customer_id):
    print("this works here")
    context = {
        "customer_id": customer_id,
        "customer": Customer.objects.get(id=customer_id),
        "cards": Customer_payment.objects.filter(customer_payment=customer_id),
    }

    return render(request, "customer_account.html", context)


def customer_account_edit(request, customer_id):

    customer = Customer.objects.filter(
        first_name=request.session["customer_first_name"]
    )
    if customer:
        logged_customer = customer[0]
        if bcrypt.checkpw(
            request.POST["password"].encode(), logged_customer.password.encode()
        ):
            password_from_form = request.POST["new_password"]
            pw_hash = bcrypt.hashpw(
                password_from_form.encode(), bcrypt.gensalt()
            ).decode()

    c = Customer.objects.get(id=customer_id)
    c.profile = request.POST["profile"]
    c.first_name = request.POST["first_name"]
    c.last_name = request.POST["last_name"]
    c.email = request.POST["email"]
    c.password = pw_hash
    c.mobile = request.POST["mobile"]
    c.driving_license = request.FILES["driving_license"]
    c.save()

    return redirect("/my_dashboard/customer_account/" + customer_id)


def contact(request):
    return render(request, "contact.html")


def delete_car(request, car_id):

    c = Car.objects.get(id=car_id)
    c.delete()

    return redirect("/my_dashboard/add_car")


def customer_add_payment(request, customer_id):

    # card_number_from_form = request.POST["card_number"]
    # car_number_hash = bcrypt.hashpw(card_number_from_form.encode(), bcrypt.gensalt()).decode()
    # cvv_from_form = request.POST["cvv"]
    # cvv_hash = bcrypt.hashpw(cvv_from_form.encode(), bcrypt.gensalt()).decode()

    Customer_payment.objects.create(
        card_type=request.POST["card_type"],
        card_owner=request.POST["card_owner"],
        card_number=request.POST["card_number"],
        expiration_mm=request.POST["expiration_mm"],
        expiration_yyyy=request.POST["expiration_yyyy"],
        cvv=request.POST["cvv"],
        customer_payment=Customer.objects.get(id=customer_id),
    )

    return redirect("/my_dashboard/customer_account/" + customer_id)


def provider_add_payment(request, provider_id):

    # card_number_from_form = request.POST["card_number"]
    # car_number_hash = bcrypt.hashpw(card_number_from_form.encode(), bcrypt.gensalt()).decode()
    # cvv_from_form = request.POST["cvv"]
    # cvv_hash = bcrypt.hashpw(cvv_from_form.encode(), bcrypt.gensalt()).decode()

    Provider_payment.objects.create(
        card_owner=request.POST["card_owner"],
        card_number=request.POST["card_number"],
        expiration_mm=request.POST["expiration_mm"],
        expiration_yyyy=request.POST["expiration_yyyy"],
        cvv=request.POST["cvv"],
        provider_payment=Provider.objects.get(id=request.session["provider_id"]),
    )

    return redirect("/my_dashboard/provider_account/" + provider_id)


def customer_delete_card(request, card_id, customer_id):

    c = Customer_payment.objects.get(id=card_id)
    c.delete()

    return redirect("/my_dashboard/customer_account/" + customer_id)


def provider_delete_card(request, card_id, provider_id):

    c = Provider_payment.objects.get(id=card_id)
    c.delete()

    return redirect("/my_dashboard/provider_account/" + provider_id)
