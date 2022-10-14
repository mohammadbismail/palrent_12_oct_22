from django.urls import path
from . import views
# from django.contrib import admin

urlpatterns = [
    path("", views.my_dashboard),
    path("search/", views.customer_search),
    path("search_result/", views.customer_search_result),
    path("car_select/<car_id>/", views.customer_car_select),
    path("car_details/<car_id>/", views.customer_car_details),
    path("car_book/<car_id>/", views.customer_car_book),
    path("customer_payment_method/<customer_id>/", views.customer_payment_method),
    path("provider_payment_method/<provider_id>/", views.Provider_payment_method),
    path("customer_add_payment/<customer_id>/", views.customer_add_payment),
    path("customer_delete_card/<customer_id>/<card_id>/", views.customer_delete_card),
    path("provider_add_payment/<provider_id>/", views.provider_add_payment),
    path("provider_delete_card/<provider_id>/<card_id>/", views.provider_delete_card),
    path("payment_confirmation/<car_id>/", views.payment_confirmation),
    path("confirm_book/<car_id>/", views.confirm_book),
    path("provider_dashboard/", views.provider_dashboard),
    path("add_car/", views.add_car),
    path("insert_car/", views.insert_car),
    path("edit_car/<car_id>/", views.edit_car),
    path("edit_my_car/<car_id>/", views.edit_my_car),
    path("provider_account/<provider_id>/", views.provider_account),
    path("provider_account_edit/<provider_id>/", views.provider_account_edit),
    path("customer_account/<customer_id>/", views.customer_account),
    path("customer_account_edit/<customer_id>/", views.customer_account_edit),
    path("provider_car_details/<car_id>/", views.provider_car_details),
    path("contact/", views.contact),
    path("delete_car/<car_id>/", views.delete_car),
]
