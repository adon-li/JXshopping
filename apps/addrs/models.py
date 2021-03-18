from django.db import models

# Create your models here.

class addrs(models.Model):
    """省市区"""
    name = models.CharField(max_length=20, verbose_name='名称')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL,
                               related_name='subs',
                               null=True, blank=True,
                               verbose_name='上级行政区划')
    #related_name 关联的模型的名字，默认是类名_set,现在改为subs
    class Meta:
        db_table = 'tb_addrs'
        verbose_name = '省市区'
        verbose_name_plural = '省市区'
    def __str__(self):
        return self.name