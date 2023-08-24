from django.urls import path

from blogs import views

urlpatterns = [
    path('blog/', views.BlogView.as_view({"post": "create"})),  # 添加資源
]
