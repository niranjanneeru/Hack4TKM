from django.urls import path

from .views import blog_view, blog_create_view, tag_view
from ..registrations.views import topper_view,winner_view

app_name = "blog"
urlpatterns = [
    path('', blog_view, name='blogs'),
    path('create/', blog_create_view, name='create_blogs'),
    path('tags/', tag_view, name="tags"),
    path('top/', topper_view, name='topper'),
    path('winner/',winner_view,name='winner')
]
