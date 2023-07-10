from rest_framework import permissions

from users.models import API


class UserPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user  # 判斷操作的數據對象(用戶)和登錄的用戶對象是否是同一個用戶


class APIPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # 視圖函數繼承ViewSet情況下,view才有action屬性,否則使用request.method屬性
        action = getattr(view, 'action', request.method)
        api = f"{view.__class__.__module__}.{view.__class__.__name__}.{action}"
        print(api, request.method, request.user)

        if not request.user.is_authenticated:  # 如果沒有登錄,使用預置的AnonymousUser查詢角色
            return API.objects.filter(api=api, role__name='AnonymousUser').exists()
        if roles := request.user.role.all():  # 檢查當前用戶的所有角色是否擁有訪問當前API的權限
            return API.objects.filter(api=api, role__in=roles).exists()
        # 如果當前用戶還沒有分配角色,使用預置的NormalUser查詢角色
        return API.objects.filter(api=api, role__name='NormalUser').exists()
