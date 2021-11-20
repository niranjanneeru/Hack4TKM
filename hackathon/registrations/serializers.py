from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework.serializers import ModelSerializer, Serializer, CharField, EmailField, IntegerField

from .models import Registrations, TeamMember, FAQ, Sponsors


class TeamMemberSerializer(ModelSerializer):
    class Meta:
        model = TeamMember
        fields = ['name', 'discord_id', 'email_id', 'phone_no', 'college_name', 'address', 'district', 'state',
                  'pincode']


class RegSerializer(ModelSerializer):
    team = TeamMemberSerializer(many=True)

    class Meta:
        model = Registrations
        fields = '__all__'

    def create(self, validated_data):
        team = validated_data.pop('team')
        reg = Registrations.objects.create(**validated_data)
        for member in team:
            TeamMember.objects.create(**member, team=reg)
        validated_data['team'] = team
        return validated_data


class TeamRegSerializer(Serializer):
    team = RegSerializer()
    members = TeamMemberSerializer(many=True)

    def create(self, validated_data):
        print(validated_data)
        reg = RegSerializer(data=validated_data.pop('team'))
        reg.is_valid()
        reg.save()
        mem = TeamMemberSerializer(data=validated_data.pop('members'), many=True)
        print(validated_data)
        mem.is_valid(raise_exception=True)
        mem.save()


class MobileSerializer(Serializer):
    phone_no = PhoneNumberField()


class PaymentConfirmationSerializer(Serializer):
    payment_id = CharField(max_length=50)
    order_id = CharField(max_length=50)
    signature = CharField(max_length=500)


class FAQSerializer(ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'


class SponsorSerializer(ModelSerializer):
    class Meta:
        model = Sponsors
        fields = '__all__'


class ProfileSerializer(Serializer):
    name = CharField(max_length=50)
    discord_id = CharField(max_length=30)
    email_id = EmailField(max_length=100)
    phone_no = PhoneNumberField()
    college_name = CharField(max_length=50)
    team_members = IntegerField(default=1)
    address = CharField(max_length=1000)
    district = CharField(max_length=50)
    state = CharField(max_length=50)
    pincode = IntegerField()


class TeamNameSerializer(Serializer):
    team_name = CharField(max_length=30)
