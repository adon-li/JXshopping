from django.db import models

# Create your models here.
from utils.models import BaseModel

class OauthQQUser(BaseModel):
    username = models.ForeignKey('users.User',on_delete=models.CASCADE,verbose_name='用户')
    openid = models.CharField(max_length=64,verbose_name='openid',db_index=True)

    class Meta:
        db_table = 'tb_oauth_login_qq'
        verbose_name = 'QQ登录用户数据'
        verbose_name_plural = verbose_name