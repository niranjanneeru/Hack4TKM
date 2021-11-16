from rest_framework.serializers import ModelSerializer

from .models import Registrations, TeamMember


class TeamMemberSerializer(ModelSerializer):
    class Meta:
        model = TeamMember
        fields = ['name', 'discord_id', 'email_id', 'phone_no', 'college_name']


class RegSerializer(ModelSerializer):
    team_members = TeamMemberSerializer(many=True)

    class Meta:
        model = Registrations
        # read_only_fields = ('id', 'have_complete', 'partner')
        fields = '__all__'

    def create(self, validated_data):
        print(validated_data)
        data = validated_data.pop('team_members')
        reg = Registrations.objects.create(**validated_data)
        for member in data:
            TeamMember.objects.create(team=reg, **member)
        return reg
