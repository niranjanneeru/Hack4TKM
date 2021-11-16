from rest_framework.serializers import ModelSerializer

from .models import Registrations


class RegSerializer(ModelSerializer):
    class Meta:
        model = Registrations
        # read_only_fields = ('id', 'have_complete', 'partner')
        fields = '__all__'
