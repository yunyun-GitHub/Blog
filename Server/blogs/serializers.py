import re
from rest_framework import serializers
from blogs.models import Blog, Image


class BlogSerializer(serializers.ModelSerializer):
    """博客模型的序列化器"""
    author = serializers.CharField(source='author.username', read_only=True)
    authorId = serializers.CharField(source='author.id', read_only=True)

    class Meta:
        model = Blog
        fields = ['id', 'title', 'authorId', 'author', 'update_time', 'content']

    def validate(self, data):
        # 多字段的联合唯一性约束
        if Blog.objects.filter(title=data.get('title'), author=self.context.get('request').user).exists():
            raise serializers.ValidationError({'title': '標題已存在'})
        return data

    def create(self, validated_data):
        author = self.context.get('request').user
        validated_data['author'] = author  # 作者字段由後端生成
        instance = super().create(validated_data)  # 創建博客

        pattern = re.compile(r'<img .*?src="/media/(%s/blog/image/.*?)".*?>' % re.escape(str(author)))
        images = re.findall(pattern, validated_data.get('content'))  # 匹配所有的圖片

        Image.objects.filter(author=author, blog__isnull=True, image__in=images).update(blog=instance)  # 為使用的圖片設置blog字段
        Image.objects.filter(author=author, blog__isnull=True).delete()  # 刪除多餘的圖片(上傳後又沒使用)

        return instance

    def update(self, instance, validated_data):
        author = instance.author  # 在正則表達式中使用變量, 需要使用%s字符串格式化
        pattern = re.compile(r'<img .*?src="/media/(%s/blog/image/.*?)".*?>' % re.escape(str(author)))
        images = re.findall(pattern, validated_data.get('content', instance.content))  # 匹配所有的圖片

        Image.objects.filter(author=author, blog=instance).exclude(image__in=images).delete()  # 更新被刪除的圖片
        Image.objects.filter(author=author, blog__isnull=True, image__in=images).update(blog=instance)  # 為使用的圖片設置blog字段
        Image.objects.filter(author=author, blog__isnull=True).delete()  # 刪除多餘的圖片(上傳後又沒使用)

        return super().update(instance, validated_data)


class ImageSerializer(serializers.ModelSerializer):
    """上传图片的序列化器"""
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())  # 作者字段由後端自動生成
    image = serializers.ImageField(use_url=False)  # 只需要不帶域名的相對路徑

    class Meta:
        model = Image
        fields = ['image', 'author']
