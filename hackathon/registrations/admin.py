import nested_admin
from django.contrib import admin

from .models import TeamMember, Registrations, Payment

admin.site.register(Payment)


class TeamMemberNestedAdmin(nested_admin.NestedStackedInline):
    model = TeamMember
    extra = 0


@admin.register(Registrations)
class RegistrationAdmin(nested_admin.NestedModelAdmin):
    list_display = ['team_name', 'name', 'team_members', 'discord_id', 'college_name']
    list_filter = ['college_name', 'date', 'team__college_name']
    search_fields = ['name', 'team__name', 'discord_id', 'team__discord_id', 'email_id', 'team__email_id', 'phone_no',
                     'team__phone_no', 'team_name', 'college_name', 'team__college_name']
    list_per_page = 50
    inlines = [TeamMemberNestedAdmin, ]
