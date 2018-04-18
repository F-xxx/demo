from django.db import models

# Create your models here.

class GameInfo(models.Model):
    plat_choice = (
        ('ios','iOS'),
        ('gp', 'Google-Android'),
    )
    opt_choice = (
        ('b', 'Battle'),
        ('g', 'GateWay'),
    )
    zone_choice = (
        ('w','23-华盛顿'),
        ('l','107-洛杉矶'),
    )
    platform = models.CharField(choices=plat_choice,default='ios',max_length=64,verbose_name='选择平台')
    operate = models.CharField(choices=opt_choice,default='b',max_length=64,verbose_name='选择操作')
    zone = models.CharField(choices=zone_choice,default='w',max_length=64,verbose_name='选择地区')

class UpdateInfo(models.Model):
    date = models.DateTimeField(auto_now=True)
    total = models.IntegerField()

