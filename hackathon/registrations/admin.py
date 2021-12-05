import csv
from typing import Union, List

import nested_admin
from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpResponse

from .models import TeamMember, Registrations, Payment, FAQ, Sponsors, Top, Winner

admin.site.register(Payment)
admin.site.register(FAQ)
admin.site.register(Sponsors)


class ExportCSVMixin:
    def export_as_csv(self, request, queryset: Union[QuerySet, List[Registrations]]):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=registration.csv'
        writer = csv.writer(response)

        sub_field_names = [field.name for field in TeamMember._meta.fields]
        payment_fields = [field.name for field in Payment._meta.fields]
        writer.writerow(field_names + payment_fields + (sub_field_names * 4))
        for obj in queryset:
            res = [getattr(obj, field) for field in field_names]
            for info in obj.payment.all():
                res = res + [getattr(info, field) for field in payment_fields]
            for sub_obj in obj.team.all():
                res = res + [getattr(sub_obj, field) for field in sub_field_names]
            row = writer.writerow(res)

        return response

    export_as_csv.short_description = "Export CSV"


class TeamMemberNestedAdmin(nested_admin.NestedStackedInline):
    model = TeamMember
    extra = 0


class PaymentNestedAdmin(nested_admin.NestedStackedInline):
    model = Payment
    extra = 0


@admin.register(Registrations)
class RegistrationAdmin(nested_admin.NestedModelAdmin, ExportCSVMixin):
    list_display = ['team_name', 'name', 'has_paid', 'team_members', 'discord_id', 'college_name']
    list_filter = ['college_name', 'date', 'team__college_name', 'payment__has_paid']
    search_fields = ['name', 'team__name', 'discord_id', 'team__discord_id', 'email_id', 'team__email_id', 'phone_no',
                     'team__phone_no', 'team_name', 'college_name', 'team__college_name', 'payment__id',
                     'payment__payment_id']
    list_per_page = 50
    actions = ["export_as_csv", ]
    inlines = [TeamMemberNestedAdmin, PaymentNestedAdmin]

    def has_paid(self, obj):
        obj = obj.payment.all()
        if obj:
            if obj[0].has_paid:
                return "Yes"
        return "No"


admin.site.register(Top)
admin.site.register(Winner)
