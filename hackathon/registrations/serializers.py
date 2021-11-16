from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework.serializers import ModelSerializer, Serializer, CharField

from .models import Registrations, TeamMember


class TeamMemberSerializer(ModelSerializer):
    class Meta:
        model = TeamMember
        fields = ['name', 'discord_id', 'email_id', 'phone_no', 'college_name']


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
