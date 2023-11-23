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
        # 多字段的联合唯一性约束, 排除更新时因为与自己比较而触发唯一性约束
        if Blog.objects.filter(title=data.get('title'), author=self.context.get('request').user).exclude(
                pk=getattr(self.instance, 'pk', None)).exists():
            raise serializers.ValidationError({'title': '標題已存在'})
        return data

    def create(self, validated_data):
        validated_data['author'] = self.context.get('request').user  # 作者字段由後端生成
        return super().create(validated_data)

    def save(self, **kwargs):
        instance = super().save(**kwargs)  # 調用父類方法
        self.process_images()  # 處理圖片
        return instance

    def process_images(self):
        """處理圖片"""
        author = self.instance.author  # 在正則表達式中使用變量, 需要使用%s字符串格式化
        pattern = re.compile(r'<img .*?src="/media/(%s/blog/image/.*?)".*?>' % re.escape(author.username))
        images = re.findall(pattern, self.instance.content)  # 匹配所有的圖片

        # 刪除被刪除的圖片, 為使用的圖片設置blog字段, 刪除多餘的圖片(上傳後又沒使用)
        Image.objects.filter(author=author, blog=self.instance).exclude(image__in=images).delete()
        Image.objects.filter(author=author, blog__isnull=True, image__in=images).update(blog=self.instance)
        Image.objects.filter(author=author, blog__isnull=True).delete()


class ImageSerializer(serializers.ModelSerializer):
    """上传图片的序列化器"""
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())  # 作者字段由後端自動生成
    image = serializers.ImageField(use_url=False)  # 只需要不帶域名的相對路徑

    class Meta:
        model = Image
        fields = ['image', 'author']
