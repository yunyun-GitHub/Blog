import os

from django.db import models
from common.db import BaseModel
from django.contrib.auth.models import AbstractUser  # django中自帶的用戶認證模型


def get_image_path(instance, filename):
    # You can write your own logic here to generate a unique path
    return os.path.join(str(instance.username), "avatar", filename)


class User(AbstractUser, BaseModel):
    """用戶模型"""
    email = models.EmailField(verbose_name='郵箱', unique=True)
    avatar = models.ImageField(verbose_name='用戶頭像', upload_to=get_image_path, blank=True, null=True)
    role = models.ManyToManyField('Role', related_name='user', blank=True)

    class Meta:
        db_table = 'users'
        verbose_name = '用戶表'
        verbose_name_plural = verbose_name


class Role(BaseModel):
    """角色模型"""
    name = models.CharField(verbose_name='角色名', max_length=32, unique=True)
    api = models.ManyToManyField('API', related_name='role', blank=True)

    class Meta:
        db_table = 'role'
        verbose_name = '角色表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class API(models.Model):
    name = models.CharField(verbose_name='API名稱', max_length=32, unique=True)
    api = models.CharField(verbose_name='API信息', max_length=128, unique=True)

    class Meta:
        db_table = 'api'
        verbose_name = 'API信息'
        verbose_name_plural = 'API信息'

    def __str__(self):
        return self.name


class SMSCode(BaseModel):
    """驗證碼模型"""
    email = models.EmailField(verbose_name='郵箱')
    code = models.CharField(max_length=6, verbose_name='驗證碼')

    class Meta:
        db_table = 'smscode'
        verbose_name = '驗證碼表'
        verbose_name_plural = verbose_name
