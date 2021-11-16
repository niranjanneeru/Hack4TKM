import razorpay
from django.conf import settings
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from .models import Registrations, Payment
from .serializers import RegSerializer
from .utils import amount


class RegisterView(CreateAPIView):
    serializer_class = RegSerializer

    def create(self, request, *args, **kwargs):
        serializer: RegSerializer = self.serializer_class(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # serializer.save()
        team = Registrations.objects.get(discord_id=serializer.initial_data['discord_id'])
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        client.set_app_details({"title": "Hack4TKM", "version": "v1"})
        data = {
            'amount': amount(team),
            'currency': "INR"
        }
        payment = client.order.create(data=data)
        Payment.objects.create(team=team, id=payment['id'], amount=payment['amount'])
        return Response({"Df": "serializer.data"}, status.HTTP_201_CREATED)


reg_view = RegisterView.as_view()
