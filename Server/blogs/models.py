from django.db import models

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
