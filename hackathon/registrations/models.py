from django.db import models
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class Registrations(models.Model):
    name = models.CharField(_("Team Leader"), max_length=50)
    discord_id = models.CharField(max_length=30, unique=True)
    email_id = models.EmailField(max_length=100, unique=True)
    phone_no = PhoneNumberField(_("Phone Number"), unique=True)
    team_name = models.CharField(max_length=30)
    college_name = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now=True)
    team_members = models.PositiveSmallIntegerField(null=True, blank=True, default=1)

    def __str__(self):
        return f"{self.team_name}: {self.name}"

    class Meta:
        verbose_name_plural = "Registrations"
        verbose_name = "Registration"


class TeamMember(models.Model):
    team = models.ForeignKey(Registrations, on_delete=models.CASCADE, related_name='team')
    name = models.CharField(max_length=50)
    discord_id = models.CharField(max_length=30, unique=True)
    email_id = models.EmailField(max_length=100, null=True, blank=True)
    phone_no = PhoneNumberField(_("Phone Number"), unique=True)
    college_name = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.team.team_name}: {self.name}"


class Payment(models.Model):
    team = models.ForeignKey(Registrations, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    amount = models.FloatField()
    id = models.CharField(max_length=200, primary_key=True)
    has_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.team.team_name
