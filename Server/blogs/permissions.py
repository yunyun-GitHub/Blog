from rest_framework import permissions


class BlogPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['DELETE', 'PUT', 'PATCH']:
            return obj.author == request.user  # 判斷操作的數據對象(用戶)和登錄的用戶對象是否是同一個用戶
        return True
