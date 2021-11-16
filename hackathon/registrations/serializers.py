from rest_framework.serializers import ModelSerializer, Serializer

from .models import Registrations, TeamMember


class TeamMemberSerializer(ModelSerializer):
    class Meta:
        model = TeamMember
        fields = ['name', 'discord_id', 'email_id', 'phone_no', 'college_name']


class RegSerializer(ModelSerializer):
    class Meta:
        model = Registrations
        fields = '__all__'


class TeamRegSerializer(Serializer):
    team = RegSerializer()
    members = TeamMemberSerializer(many=True)

    def create(self, validated_data):
        team = validated_data.pop('team')
        reg = RegSerializer(data=team)
        reg.is_valid()
        reg = reg.save()
        members = validated_data.pop('members')
        for member in members:
            t = TeamMember(**member, team=reg)
            t.save()

        return {'team': team, 'members': members}
