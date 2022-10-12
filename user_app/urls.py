from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard),
    path("search/", views.search),
    path("search_result/", views.search_result),
    path("car_select/<car_id>/", views.car_select),
    path("car_details/<car_id>/", views.car_details),
    path("car_book/<car_id>/", views.car_book),
    path("login/", views.login),
    path("register/", views.register),
    path("customer_register/", views.customer_register),
    path("provider_register/", views.provider_register),
    path("delete/", views.delete),
    path("contact/", views.contact),
]
