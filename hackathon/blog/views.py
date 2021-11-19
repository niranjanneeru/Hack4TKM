from typing import Any

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from hackathon.blog.models import Blog, Tags
from .serializers import BlogSerializer, BlogWriteSerializer, TagSerializer


class BlogView(ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    filter_backends = [DjangoFilterBackend, ]
    filterset_fields = ['tags__name', ]

    def get_queryset(self):
        return self.queryset.filter(is_verified=True)


blog_view = BlogView.as_view()


class BlogCreateView(CreateAPIView):
    serializer_class = BlogWriteSerializer

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        ser = BlogWriteSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        tags = ser.validated_data.pop('tags').split(',')
        a = ser.save()
        objs = []
        for tag in tags:
            obj, created = Tags.objects.get_or_create(name=tag.strip(), defaults={'name': tag.strip()})
            objs.append(obj)
        a.tags.set(objs)
        a.save()
        return Response({'details': 'Submitted for Approval'}, status=status.HTTP_200_OK)


blog_create_view = BlogCreateView.as_view()


class TagView(ListAPIView):
    queryset = Tags.objects.all()
    serializer_class = TagSerializer


tag_view = TagView.as_view()
