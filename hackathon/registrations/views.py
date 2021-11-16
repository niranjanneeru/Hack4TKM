from rest_framework.generics import CreateAPIView

from .serializers import RegSerializer


class RegisterView(CreateAPIView):
    serializer_class = RegSerializer


reg_view = RegisterView.as_view()
