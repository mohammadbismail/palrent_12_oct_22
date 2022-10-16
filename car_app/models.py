from django.db import models
from user_app.models import Customer, Provider


class Car(models.Model):
    brand = models.CharField(max_length=45)
    model = models.CharField(max_length=45)
    color = models.CharField(max_length=45)
    production_year = models.IntegerField()
    plate_number = models.CharField(max_length=45)
    price = models.IntegerField()
    photo = models.FileField()
    provider = models.ForeignKey(
        Provider, related_name="cars", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Booking(models.Model):
    pick_up_date = models.DateField(null=True)
    drop_off_date = models.DateField(null=True)
    status = models.CharField(max_length=45)
    customer_book = models.ForeignKey(
        Customer, related_name="customers_booked", on_delete=models.CASCADE)
    car_book = models.ForeignKey(
        Car, related_name="cars_booked", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Customer_Feedback(models.Model):
    rating = models.TextField(null=True)
    comment = models.TextField(null=True)
    customer_feedhback = models.ForeignKey(
        Customer, related_name="customers_feedback", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Car_Feedback(models.Model):
    cars = models.ManyToManyField(Car, related_name="feededbacked_cars")
    car_feedback = models.ForeignKey(
        Car, related_name="cars_feedback", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
