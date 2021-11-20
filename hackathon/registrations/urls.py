from django.urls import path

from .views import reg_view, payment_request, phone_number_view, payment_confirmation

app_name = "registrations"
urlpatterns = [
    path('', phone_number_view, name='phone_number_view'),
    path('payment/', payment_request, name='payment_view'),
    path('details/', reg_view, name='register'),
    path('confirm/', payment_confirmation, name='payment_confirmation'),
]
