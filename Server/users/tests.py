# 引入必要的模塊和Django設置
import re
import os
import sys
import django
from Server.settings import BASE_DIR

sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Server.settings")
django.setup()
from blogs.models import Image, Blog

content = '<p>請在這裏輸入内容。。。<img src="/media/Aidan/blog/image/取消_LghZ9PO.png"><img src="/media/Aidan/blog/image/拒绝_HYUtxPH.png"><img src="/media/Aidan/blog/image/返回_ikVHj9r.png"><img src="/media/Aidan/blog/image/同意.png"></p>'
author = "Aidan"
blog = Blog.objects.get(id=76)
pattern = re.compile(r'<img .*?src="/media/(%s/blog/image/.*?)".*?>' % re.escape(author))
images = re.findall(pattern, content)
print(images)

images_queryset = Image.objects.filter(author__username=author, image__in=images).update(blog=blog)

print(images_queryset)
print(blog)
