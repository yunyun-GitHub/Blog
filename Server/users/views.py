from rest_framework import mixins
from rest_framework.throttling import AnonRateThrottle
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import User, SMSCode
from users.permissions import UserPermission, APIPermission
from users.serializers import UserSerializer, SMSCodeSerializer, LoginSerializer


class LoginView(TokenObtainPairView):
    """用戶登錄"""
    serializer_class = LoginSerializer


class UserView(GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    """用戶視圖集"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [UserPermission, APIPermission]  # 設置認證用戶才能有權限訪問


class SMSCodeView(GenericViewSet, mixins.CreateModelMixin):
    """驗證碼視圖集"""
    queryset = SMSCode.objects.all()
    serializer_class = SMSCodeSerializer
    throttle_classes = [AnonRateThrottle]  # 設置限流(每分鐘只能獲取一次)
