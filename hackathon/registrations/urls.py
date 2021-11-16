from django.urls import path

from .views import reg_view

app_name = "registrations"
urlpatterns = [
    path('', reg_view, name='reg_view'),
]
