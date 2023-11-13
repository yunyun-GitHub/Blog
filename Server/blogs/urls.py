from django.urls import path

from blogs import views

urlpatterns = [
    path('blog/', views.BlogView.as_view({"post": "create", "get": "list"})),  # 增刪改查
    path('blog/<int:pk>/', views.BlogView.as_view({"get": "retrieve", "delete": "destroy", "patch": "partial_update"})),
    path('image/upload/', views.ImageView.as_view({"post": "create"})),  # 上传图片
]
