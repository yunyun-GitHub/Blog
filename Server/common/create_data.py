# 引入必要的模塊和Django設置
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Server.settings")
django.setup()

from users.models import Role, API, User


def create_role():
    """創建用戶角色"""
    role_list = [
        'AnonymousUser',
        'NormalUser',
    ]
    for role in role_list:
        if not Role.objects.filter(name=role).exists():
            Role(name=role).save()
            print(role, "成功")
        else:
            print(role, "已存在")


def create_api():
    """創建API信息"""
    api_list = [
        {'api': 'users.views.UserView.create', 'name': '注冊用戶'},
        {'api': 'users.views.UserView.retrieve', 'name': '獲取用戶信息'},
        {'api': 'users.views.UserView.partial_update', 'name': '修改用戶信息'},

        {'api': 'users.views.SMSCodeView.create', 'name': '發送驗證碼'},
    ]
    for data in api_list:
        # 检查数据是否已存在
        if not API.objects.filter(api=data['api']).exists():
            if not API.objects.filter(name=data['name']).exists():
                API(**data).save()
                print(data, "成功")
            else:
                print(data['name'], "已存在")
        else:
            print(data['api'], "已存在")


def create_admin():
    """創建admin用戶"""
    data = {'username': 'admin', 'password': 'admin', 'email': 'admin@gmail.com'}

    if not User.objects.filter(username=data['username']).exists():
        if not User.objects.filter(email=data['email']).exists():
            User.objects.create_superuser(**data)
            print(data, "成功")
        else:
            print(data['email'], "已存在")
    else:
        print(data['username'], "已存在")


create_role()  # 創建用戶角色
create_api()  # 創建API信息
create_admin()  # 創建admin用戶
