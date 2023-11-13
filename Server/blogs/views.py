from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from blogs.models import Blog, Image
from blogs.permissions import BlogPermission
from blogs.serializers import BlogSerializer, ImageSerializer
from users.permissions import APIPermission


class BlogView(ModelViewSet):
    """博客視圖集"""
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [BlogPermission, APIPermission]  # 設置認證用戶才能有權限訪問


class ImageView(GenericViewSet, mixins.CreateModelMixin):
    """上传图片視圖"""
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
