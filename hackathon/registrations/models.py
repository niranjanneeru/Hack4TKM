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
    address = models.TextField()
    district = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.IntegerField()

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
    address = models.TextField()
    district = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.IntegerField()

    def __str__(self):
        return f"{self.team.team_name}: {self.name}"


class Payment(models.Model):
    team = models.ForeignKey(Registrations, on_delete=models.CASCADE, related_name='payment')
    date = models.DateTimeField(auto_now=True)
    amount = models.FloatField()
    id = models.CharField(max_length=200, primary_key=True)
    has_paid = models.BooleanField(default=False)
    payment_id = models.CharField(max_length=50, null=True, blank=True)
    signature = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.team.team_name


class Sponsors(models.Model):
    image_link = models.URLField(max_length=500)
    link = models.URLField(max_length=500)
    name = models.CharField(max_length=100)
    order = models.IntegerField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order', ]
        verbose_name_plural = "Sponsors"
        verbose_name = "Sponsor"


class FAQ(models.Model):
    ques = models.CharField(max_length=500)
    ans = models.CharField(max_length=500)
    order = models.IntegerField(unique=True)

    def __str__(self):
        return str(self.order)

    class Meta:
        ordering = ['order', ]
        verbose_name_plural = "FAQs"
        verbose_name = "FAQ"
