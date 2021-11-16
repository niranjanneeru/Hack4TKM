from rest_framework.generics import ListCreateAPIView

from .models import Registrations
from .serializers import RegSerializer


class RegisterView(ListCreateAPIView):
    serializer_class = RegSerializer
    queryset = Registrations.objects.all()


reg_view = RegisterView.as_view()
