from rest_framework.generics import ListAPIView

from hackathon.blog.models import Blog
from .serializers import BlogSerializer


class BlogView(ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer


blog_view = BlogView.as_view()
