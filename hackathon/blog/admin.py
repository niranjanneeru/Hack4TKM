from django.contrib import admin

# Register your models here.
from hackathon.blog.models import Blog, Tags

admin.site.register(Tags)


@admin.register(Blog)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'rating', 'is_verified']
    list_filter = ['is_verified', ]
    list_per_page = 50

