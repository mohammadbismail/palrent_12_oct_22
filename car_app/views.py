
from django.shortcuts import render, redirect
from user_app.models import Provider, Customer
from .models import Car
import bcrypt


def my_dashboard(request):

    if "customer_id" not in request.session:
        return redirect("/")

    customer_id = request.session["customer_id"]

    context = {
        'customer_id': customer_id
    }


    return render(request,"my_dashboard.html", context)

def search(request):

    # request.session["location"] = request.POST["location"]
    # request.session["pick_up_date"] = request.POST["pick_up_date"]
    # request.session["drop_off_date"] = request.POST["drop_off_date"]

    return redirect("/my_dashboard/search_result")

def search_result(request):

    context = {
        'searched_cars': Provider.objects.filter(location=request.POST["location"])
    }

    return render(request,"search_result.html", context)

def car_select(request, car_id):
    return redirect("/my_dashboard/car_details/"+car_id)


def car_details(request, car_id):
    context = {
        'selected_car': Car.objects.get(id=car_id)
    }
    return render(request,"car_details.html", context)


def car_book(request, car_id):

    return redirect("/my_dashboard/payment_confirmation/"+car_id)


def provider_dashboard(request):
    
    print("this works here")
    context = {
        'cars': Car.objects.filter(id=request.session['provider_id']),

    }
    return render(request,"provider_dashboard.html", context)


def car_book(request):
    return redirect("/my_dashboard/payment_confirmation")


def payment_method(request):
    return render(request,"payment_method.html")


def payment_confirmation(request, car_id):

    context = {
        'car_id': car_id
    }

    return render(request,"payment_confirmation.html", context)


def confirm_book(request):
    return redirect("/my_dashboard")




def add_car(request):
    print("this works here")

    context = {
        'garage': Car.objects.filter(provider=request.session["provider_id"])
    }
    return render(request,"add_car.html", context)

def insert_car(request):

    Car.objects.create(
            brand = request.POST['brand'],
            model = request.POST['model'],
            color = request.POST['color'],
            production_year = request.POST['production_year'],
            plate_number = request.POST['plate_number'],
            price = request.POST['price'],
            provider = Provider.objects.get(id=request.session['provider_id'])
        )
    return redirect("/my_dashboard/add_car")

def edit_car(request, car_id):

    context = {
        'garage': Car.objects.filter(provider=request.session["provider_id"]),
        'car_id': car_id,
        'car': Car.objects.get(id=car_id)
    }
    return render(request,"edit_car.html", context)

def edit_my_car(request, car_id):

    print("this works here")

    # car_id = request.POST['car_id']
    c = Car.objects.get(id=car_id)
    c.brand = request.POST['brand']
    c.model = request.POST['model']
    c.color = request.POST['color']
    c.production_year = request.POST['production_year']
    c.plate_number = request.POST['plate_number']
    c.price = request.POST['price']
    c.save()

    return redirect("/my_dashboard/edit_car/"+car_id)


def provider_account(request, provider_id):
    print("this works here")
    context = {
        # 'garage': Provider.objects.filter(provider=request.session["provider_id"]),
        'provider_id': provider_id,
        'provider': Provider.objects.get(id=provider_id)
    }

    return render(request,"provider_account.html", context)


def provider_account_edit(request, provider_id):

    provider = Provider.objects.filter(name=request.session["provider_name"])
    if provider:
        logged_provider = provider[0]
        if bcrypt.checkpw(request.POST["password"].encode(), logged_provider.password.encode()):
            password_from_form = request.POST["new_password"]
            pw_hash = bcrypt.hashpw(password_from_form.encode(), bcrypt.gensalt()).decode()

    

    c = Provider.objects.get(id=provider_id)
    c.name = request.POST['name']
    c.location = request.POST['location']
    c.email = request.POST['email']
    c.password = pw_hash
    c.permit = request.POST['permit']
    c.mobile = request.POST['mobile']
    c.save()

    return redirect("/my_dashboard/provider_account/"+provider_id)


def provider_car_details(request, car_id):
    print('thisworks here')
    context = {
        'selected_car': Car.objects.get(id=car_id)
    }
    return render(request,"provider_car_details.html", context)


def customer_account(request, customer_id):
    print("this works here")
    context = {
        'customer_id': customer_id,
        'customer': Customer.objects.get(id=customer_id)
    }

    return render(request,"customer_account.html", context)


def customer_account_edit(request, customer_id):

    customer = Customer.objects.filter(name=request.session["customer_first_name"])
    if customer:
        logged_customer = customer[0]
        if bcrypt.checkpw(request.POST["password"].encode(), logged_customer.password.encode()):
            password_from_form = request.POST["new_password"]
            pw_hash = bcrypt.hashpw(password_from_form.encode(), bcrypt.gensalt()).decode()

    

    c = Customer.objects.get(id=customer_id)
    c.first_name = request.POST['first_name']
    c.last_name = request.POST['last_name']
    c.email = request.POST['email']
    c.password = pw_hash
    c.national_id = request.POST['national_id']
    c.mobile = request.POST['mobile']
    c.save()

    return redirect("/my_dashboard/customer_account/"+customer_id)

def contact(request):
    return render(request, 'contact.html')