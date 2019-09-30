from django.db import models
# Create your models here.

from django.utils import timezone
from django.contrib.auth.models import User


class myrecord(models.Model):
    op = models.CharField(max_length=100)
    # 操作决定结果返回形式：文字/图片/文字+图片
    created_at = models.DateTimeField(default=timezone.now)
    # 当前时间戳
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    # 绑定用户
    image_input = models.ImageField(upload_to='input',default='')
    # 用户输出需要处理的图片
    image_output = models.ImageField(upload_to='output',default='', null=True,blank=True)
    # 图片处理结果的图片信息
    info_output = models.TextField(default='', null=True,blank=True)
    # 图片处理结果的文字信息

    def __str__(self):
        return self.owner.username+'-'+self.op
