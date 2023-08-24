from rest_framework import serializers

from blogs.models import Blog


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['title', 'content']

    def validate(self, data):
        data['author'] = self.context.get('request').user  # 作者字段由後端生成
        if Blog.objects.filter(title=data['title'], author=data['author']).exists():
            raise serializers.ValidationError({'title': '標題已存在'})
        return data
