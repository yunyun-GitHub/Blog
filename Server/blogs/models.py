import os

from django.core.files.storage import default_storage
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from common.db import BaseModel


class Blog(BaseModel):
    """博客模型"""
    author = models.ForeignKey('users.User', verbose_name='作者', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='標題', max_length=32)
    content = models.TextField(verbose_name='内容')

    class Meta:
        db_table = 'blog'
        verbose_name = '博客表'
        verbose_name_plural = verbose_name
        unique_together = [['author', 'title'], ]  # 多字段的联合唯一性约束, 这个只在数据库层面验证, 需要在序列化器中另外实现约束逻辑

    def __str__(self):
        return self.title


def get_image_path(instance, filename):
    # You can write your own logic here to generate a unique path
    return os.path.join(str(instance.author.username), "blog", "image", filename)


class Image(BaseModel):
    """圖片模型"""
    image = models.ImageField(verbose_name='圖片', upload_to=get_image_path)
    author = models.ForeignKey('users.User', verbose_name='作者', on_delete=models.CASCADE)
    blog = models.ForeignKey('Blog', verbose_name='博客', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 'image'
        verbose_name = '圖片表'
        verbose_name_plural = verbose_name


@receiver(pre_delete, sender=Image)
def image_pre_delete(sender, instance, **kwargs):
    # 刪除一條數據庫中圖片數據時, 同步刪除該圖片文件
    default_storage.delete(instance.image.name)
