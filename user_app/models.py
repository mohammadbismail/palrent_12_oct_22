from django.db import models
import re
import bcrypt
from datetime import datetime, timedelta
import os

# from car_app.models import Car

# Relation no.1
# Customer-Car (Many-->Many) car can be booked by many customers at different times
# while customer can book many cars as he desires
# ---------------------------------------------------------------------------------
# Relation no.2
# Customer-Feedback (One-->Many) customer can give many feedback on cars he booked
# while a feedback is related is coming from single customer
# ----------------------------------------------------------------------------------
# Relation no.3
# Provider-Car (One-->Many) provider can provide group of cars while car has to come from single provider
# ----------------------------------------------------------------------------------
# Relation no.4
# Car-Feedback (Many-->Many) car can have many feedbacks & feedback can be more many cars

today = datetime.today()
past_date_before_24yrs = today - timedelta(days=8760)


class CustomerManager(models.Manager):
    def customer_validator(self, data):
        errors = {}
        date_format = "%Y-%m-%d"

        EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")
        if len(data["firstName"]) < 4:
            errors["firstname"] = "Name should be more than 3 characters"
        if len(data["lastName"]) < 4:
            errors["lastname"] = "Last name should be more than 3 characters"
        if not EMAIL_REGEX.match(data["email"]):
            errors["email"] = "Invalid email address"
        if len(data["email"]) < 1:
            errors["email"] = "Email can't be empty"
        if data["password"] != data["confp"]:
            errors["password"] = "Password does not match!"
        if len(data["password"]) < 9:
            errors["password"] = "Password has to be more 8 characters length"
        if datetime.strptime(data["birthday"], date_format) > past_date_before_24yrs:
            errors["birthday"] = "Age has to be 24+ years"
        if datetime.strptime(data["birthday"], date_format) > datetime.today():
            errors["birthday"] = "Birthday should be in the past"
        return errors

    def customer_login_validator(self, data):
        errors = {}
        if data["email"] == "":
            errors["email_empty"] = "Email can't be empty!"
            return errors
        customer = Customer.objects.filter(email=data["email"])
        if not customer:
            errors["wrong_email"] = "email is not found"
            return errors
        if not bcrypt.checkpw(data["password"].encode(), customer[0].password.encode()):
            errors["wrong_password"] = "Invalid password"
        return errors


class ProviderManager(models.Manager):
    def provider_validator(self, data):
        errors = {}
        EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")
        if len(data["name"]) < 3:
            errors["name"] = "Name should be more than 8 characters"
        if len(data["location"]) < 3:
            errors["location"] = "Location should be more than 3 characters"
        if not EMAIL_REGEX.match(data["email"]):
            errors["email"] = "Invalid email address"
        if len(data["password"]) < 8:
            errors["password"] = "Password has to be more 8 characters length"
        if data["password"] != data["confp"]:
            errors["password"] = "Password does not match!"
        if len(data["mobile"]) > 10 or len(data["mobile"]) < 1:
            errors["mobile"] = "Mobile can't exceed 10 numbers and can't be empty"
        return errors

    def provider_login_validator(self, data):
        errors = {}
        if data["email"] == "":
            errors["email_empty"] = "Email can't be empty!"
            return errors
        provider = Provider.objects.filter(email=data["email"])
        if not provider:
            errors["wrong_email_c"] = "email is not found"
            return errors
        if not bcrypt.checkpw(data["password"].encode(), provider[0].password.encode()):
            errors["wrong_password"] = "Invalid password"
        return errors


class Customer(models.Model):
    profile = models.FileField(blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    mobile = models.IntegerField()
    birthday = models.DateField()
    driving_license = models.ImageField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CustomerManager()


class Provider(models.Model):
    logo = models.FileField(blank=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    mobile = models.IntegerField()
    permit = models.FileField(blank=True)
    location = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ProviderManager()
    # cars


class Customer_payment(models.Model):
    card_type = models.CharField(max_length=100)
    card_owner = models.CharField(max_length=100)
    card_number = models.IntegerField()
    expiration_mm = models.IntegerField()
    expiration_yyyy = models.IntegerField()
    cvv = models.IntegerField()
    customer_payment = models.ForeignKey(
        Customer, related_name="customer_cards", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Provider_payment(models.Model):
    card_type = models.CharField(max_length=100)
    card_owner = models.CharField(max_length=100)
    card_number = models.IntegerField()
    expiration_mm = models.IntegerField()
    expiration_yyyy = models.IntegerField()
    cvv = models.IntegerField()
    provider_payment = models.ForeignKey(
        Provider, related_name="provider_cars", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Website_review(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
