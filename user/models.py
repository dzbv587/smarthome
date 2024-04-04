from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class UserProfile(AbstractUser):
    """
    用户模型
    """
    name = models.CharField(max_length=20, default="", verbose_name="姓名")
    email = models.EmailField(max_length=30, default="", verbose_name="邮箱")
    mobile = models.CharField(max_length=11, default="", verbose_name="手机号")

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
