from django.urls import path

from .views import faq_view, sponsor_view, discord_view, team_name

app_name = "registrations"
urlpatterns = [
    path('faq/', faq_view, name='faq_view'),
    path('sponsors/', sponsor_view, name='sponsor_view'),
    path('discord/<str:discord_id>', discord_view, name='discord_view'),
    path('team/<str:discord_id>', team_name, name='team_name')
]
