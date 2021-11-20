from typing import Any

import razorpay
from django.conf import settings
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Registrations, Payment, TeamMember, FAQ, Sponsors
from .serializers import RegSerializer, MobileSerializer, TeamMemberSerializer, PaymentConfirmationSerializer, \
    FAQSerializer, SponsorSerializer, ProfileSerializer, TeamNameSerializer
from .utils import amount, send_email


class RegisterView(CreateAPIView):
    serializer_class = RegSerializer


reg_view = RegisterView.as_view()


class PhoneNumberView(CreateAPIView):
    """
    204 : New Registration
    200 : Registration Complete
    206 : Pending Payment
    """
    serializer_class = MobileSerializer

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer: MobileSerializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_no = serializer.validated_data['phone_no']
        team: Registrations = Registrations.objects.filter(phone_no=phone_no).first()
        if team:
            transaction = team.payment.first()
            data = {
                'team': RegSerializer(team).data,
                'members': TeamMemberSerializer(team.team, many=True).data,
            }
            if transaction:
                if transaction.has_paid:
                    data['detail'] = 'This Number has Registered as Team Leader and has Paid for the event'
                    return Response(data, status.HTTP_200_OK)
                else:
                    data['detail'] = 'Registered as Team Leader Payment Incomplete'
                    return Response(data, status.HTTP_206_PARTIAL_CONTENT)
            else:
                data['detail'] = 'Registered as Team Leader Payment Incomplete'
                return Response(data, status.HTTP_206_PARTIAL_CONTENT)
        member: TeamMember = TeamMember.objects.filter(phone_no=phone_no).first()
        if member:
            transaction = member.team.payment.first()
            team = member.team
            data = {
                'team': RegSerializer(team).data,
                'members': TeamMemberSerializer(team.team, many=True).data
            }
            if transaction:
                if transaction.has_paid:
                    data['detail'] = 'This Number has Registered and has Paid for the event'
                    return Response(data, status.HTTP_200_OK)
                else:
                    data['detail'] = 'This Number has Registered Payment Incomplete'
                    return Response(data, status.HTTP_208_ALREADY_REPORTED)
            else:
                data['detail'] = 'This Number has Registered Payment Incomplete'
                return Response(data, status.HTTP_208_ALREADY_REPORTED)
        return Response({'detail': 'Registration Pending'}, status.HTTP_204_NO_CONTENT)


phone_number_view = PhoneNumberView.as_view()


class PaymentRequest(CreateAPIView):
    """
    Payment Id, Amount for Razor Pay
    """
    serializer_class = MobileSerializer

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer: MobileSerializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_no = serializer.validated_data['phone_no']
        team: Registrations = Registrations.objects.filter(phone_no=phone_no).first()
        if not team:
            return Response({'detail': 'No Registration Found'}, status.HTTP_404_NOT_FOUND)
        if team.payment.filter(has_paid=True):
            return Response({"detail": "Existing Successful Payment"}, status.HTTP_200_OK)
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        client.set_app_details({"title": "Hack4TKM", "version": "v1"})
        old_payment = team.payment.filter(has_paid=False)
        if old_payment:
            obj = old_payment[0]
            payment = client.order.fetch(obj.id)
        else:
            data = {
                'amount': amount(team),
                'currency': "INR"
            }
            payment = client.order.create(data=data)
            Payment.objects.create(team=team, id=payment['id'], amount=payment['amount'])
        payment['RAZORPAY_KEY_ID'] = settings.RAZORPAY_KEY_ID
        payment['call_back_url'] = 'https://api.hack4tkm.in/register/confirm/'

        return Response({'payment': payment, 'team': RegSerializer(team).data,
                         'members': TeamMemberSerializer(team.team.all(), many=True).data},
                        status.HTTP_201_CREATED)


payment_request = PaymentRequest.as_view()


class PaymentConfirmationView(CreateAPIView):
    serializer_class = PaymentConfirmationSerializer

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = PaymentConfirmationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order_id = serializer.validated_data['order_id']
        payment_id = serializer.validated_data['payment_id']
        obj: Payment = Payment.objects.filter(id=order_id).first()
        if obj:
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            client.set_app_details({"title": "Hack4TKM", "version": "v1"})
            payments = client.order.payments(order_id)
            for payment in payments['items']:
                params_dict = {
                    'razorpay_order_id': order_id,
                    'razorpay_payment_id': payment_id,
                    'razorpay_signature': serializer.validated_data['signature']
                }

                result = client.utility.verify_payment_signature(params_dict)
                if result is None and payment["status"] == "captured":
                    obj.payment_id = payment_id
                    obj.has_paid = True
                    obj.signature = serializer.validated_data['signature']
                    obj.save()
                    send_email(obj)
                    return Response({'detail': 'Payment Successful'}, status.HTTP_201_CREATED)
                else:
                    return Response({"detail": "Unsuccessful Payment Payment Hashes Mismatch"},
                                    status=status.HTTP_402_PAYMENT_REQUIRED)
            else:
                return Response({'detail': "Payment Not Recorded"}, status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'detail': 'No Such Transaction'}, status.HTTP_400_BAD_REQUEST)


payment_confirmation = PaymentConfirmationView.as_view()


class FAQView(ListAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer


faq_view = FAQView.as_view()


class SponsorView(ListAPIView):
    queryset = Sponsors.objects.all()
    serializer_class = SponsorSerializer


sponsor_view = SponsorView.as_view()


class DiscordView(RetrieveAPIView):
    queryset = Registrations.objects.all()
    lookup_field = 'discord_id'
    serializer_class = ProfileSerializer

    def retrieve(self, request: Request, *args: Any, **kwargs: Any):
        discord_id = kwargs['discord_id']
        team = Registrations.objects.filter(discord_id=discord_id).first()
        if team:
            return Response(ProfileSerializer(team).data, status.HTTP_200_OK)
        else:
            member = TeamMember.objects.filter(discord_id=discord_id).first()
            if member:
                return Response(ProfileSerializer(member).data, status.HTTP_200_OK)
        return Response({'detail': 'Not Found'}, status.HTTP_404_NOT_FOUND)


discord_view = DiscordView.as_view()


class TeamNameView(RetrieveAPIView):
    serializer_class = TeamNameSerializer
    queryset = Registrations.objects.all()
    lookup_field = 'discord_id'

    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        discord_id = kwargs['discord_id']
        team = Registrations.objects.filter(discord_id=discord_id).first()
        if team:
            return Response(TeamNameSerializer(team).data, status.HTTP_200_OK)
        else:
            member: TeamMember = TeamMember.objects.filter(discord_id=discord_id).first()
            if member:
                team = member.team
                return Response(TeamNameSerializer(team).data, status.HTTP_200_OK)
        return Response({'detail': 'Not Found'}, status.HTTP_404_NOT_FOUND)


team_name = TeamNameView.as_view()
