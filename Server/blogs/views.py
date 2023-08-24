from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from blogs.models import Blog
from blogs.serializers import BlogSerializer


class BlogView(GenericViewSet, mixins.CreateModelMixin):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    # permission_classes = []  # 設置認證用戶才能有權限訪問
