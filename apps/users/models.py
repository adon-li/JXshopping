from django.db import models

# from django.contrib.auth.models import User
"""
Django自带的用户模型（密码加密）
AbstractBaseUser类定义了password，last_login。密码有加密
AbstractUser继承了AbstractBaseUser并重写了username，first_name，last_name，email，
"""
from django.contrib.auth.models import AbstractUser
class User(AbstractUser):
    mobile=models.CharField(max_length=11,unique=True)
    email_active = models.BooleanField(default=False,verbose_name='邮箱验证状态')
    class Meta:
        db_table='tb_users'
        verbose_name='用户管理'
        verbose_name_plural=verbose_name#复数变为单数
    # def __str__(self):
    #     return self.username