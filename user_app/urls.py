from django.urls import path
from . import views


urlpatterns = [
    path("", views.dashboard),
    # path("my_dashboard/", views.my_dashboard),
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
    path("delete_account/", views.delete_account),
    path("contact/", views.contact),
<<<<<<< HEAD
    path("website_review/", views.website_review),
]
=======
>>>>>>> 04659b98dd36bf3fb8f59ca94344e24b9e8f7304

    path('check_email/<email>', views.check_email),
]
