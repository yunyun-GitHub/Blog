# Generated by Django 4.2.2 on 2023-08-10 01:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0004_alter_blog_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='blog',
            unique_together=set(),
        ),
    ]
