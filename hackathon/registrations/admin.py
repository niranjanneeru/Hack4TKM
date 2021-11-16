from django.contrib import admin

from .models import TeamMember, Payment, Registrations

admin.site.register(TeamMember)
admin.site.register(Payment)
admin.site.register(Registrations)
