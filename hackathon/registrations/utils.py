from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import get_template

from hackathon.registrations.models import Registrations, Payment


def amount(team: Registrations):
    team.team_members = len(team.team.all()) + 1
    team.save()
    return team.team_members * settings.AMOUNT * 100


def send_email(payment: Payment):
    team = payment.team
    mail_ids = [team.email_id, ]
    for team_member in team.team.all():
        mail_ids.append(team_member.email_id)
    message = get_template("emails/template.html").render({'data': team})
    email = EmailMessage(
        subject="Hack4TKM",
        body=message,
        from_email=settings.EMAIL_HOST_USER,
        to=mail_ids
    )
    email.content_subtype = "html"
    # print(mail_ids)
    return email.send()
