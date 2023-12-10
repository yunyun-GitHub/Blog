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
    print("========創建用戶角色========")
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
    print("========創建API信息========")
    api_list = [
        {'api': 'users.views.UserView.create', 'name': '注冊用戶'},
        {'api': 'users.views.UserView.retrieve', 'name': '獲取用戶信息'},
        {'api': 'users.views.UserView.partial_update', 'name': '修改用戶信息'},

        {'api': 'users.views.SMSCodeView.create', 'name': '發送驗證碼'},

        {'api': 'blogs.views.BlogView.list', 'name': '獲取博客列表'},
        {'api': 'blogs.views.BlogView.create', 'name': '創建博客'},
        {'api': 'blogs.views.BlogView.retrieve', 'name': '獲取單個博客'},
        {'api': 'blogs.views.BlogView.destroy', 'name': '刪除博客'},
        {'api': 'blogs.views.BlogView.partial_update', 'name': '修改博客'},

        {'api': 'blogs.views.ImageView.create', 'name': '上传图片'},
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


def role_add_api():
    """為角色添加權限"""
    print("========為角色添加權限========")
    role_list = {
        'AnonymousUser': ['注冊用戶', '發送驗證碼', '獲取博客列表', '獲取單個博客'],
        'NormalUser': ['發送驗證碼', '獲取博客列表', '獲取單個博客', '創建博客', '刪除博客', '修改博客', '上传图片', '獲取用戶信息', '修改用戶信息'],
    }

    for role, apis in role_list.items():
        if r := Role.objects.filter(name=role).first():
            for api in apis:
                if a := API.objects.filter(name=api).first():
                    if r.api.filter(name=api).exists():
                        print(role, api, '已存在')
                    else:
                        r.api.add(a)
                        print(role, api, '添加成功')
                else:
                    print(api, '不存在')
        else:
            print(role, '不存在')


create_role()  # 創建用戶角色
create_api()  # 創建API信息
role_add_api()  # 為角色添加權限
