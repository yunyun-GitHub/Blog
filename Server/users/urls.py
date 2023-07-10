from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView, TokenObtainPairView

from users import views

urlpatterns = [
    path('token/refresh/', TokenRefreshView.as_view()),  # 刷新token
    path('token/verify/', TokenVerifyView.as_view()),  # 校驗token
    path('login/', TokenObtainPairView.as_view()),  # 登錄
    path('register/', views.UserView.as_view({"post": "create"})),  # 注冊
    path('<int:pk>/', views.UserView.as_view({"get": "retrieve"})),  # 獲取單個用戶信息的路由
    path('<int:pk>/update/', views.UserView.as_view({"patch": "partial_update"})),  # 修改用戶信息
    path('sendsms/', views.SMSCodeView.as_view({"post": "create"})),  # 發送驗證碼的接口
]
