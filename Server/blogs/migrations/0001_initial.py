# Generated by Django 4.2.2 on 2023-08-07 00:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='創建時間')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新時間')),
                ('is_delete', models.BooleanField(default=False, verbose_name='刪除標記')),
                ('title', models.CharField(max_length=32, verbose_name='標題')),
                ('content', models.TextField(verbose_name='内容')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='作者')),
            ],
            options={
                'verbose_name': '博客表',
                'verbose_name_plural': '博客表',
                'db_table': 'blogs',
                'unique_together': {('author', 'title')},
            },
        ),
    ]
