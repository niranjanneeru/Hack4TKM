from rest_framework.generics import CreateAPIView

from .models import Registrations
from .serializers import TeamRegSerializer


class RegisterView(CreateAPIView):
    serializer_class = TeamRegSerializer


reg_view = RegisterView.as_view()
