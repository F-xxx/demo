from django.db import models

# Create your models here.

class Asset(models.Model):
    asset_type_choice = (
        ('physics','物理服务器'),
        ('server','云主机'),
        ('database','云数据库实例'),
        ('nosql','非关系型数据库实例'),
        ('inside','内网服务器'),
    )
    status_choices = ((0, '在线'),
                      (1, '已下线'),
                      (2, '未知'),
                      (3, '故障'),
                      (4, '备用'),
                      )
    asset_type = models.CharField(choices=asset_type_choice,max_length=100,default='server',verbose_name='资产类型')
    name = models.CharField(max_length=100,unique=True,verbose_name='资产编号')
    loaction = models.ForeignKey('Location',related_name='location_name',verbose_name='位置')
    management_ip = models.GenericIPAddressField(blank=True,null=True,verbose_name='管理IP')
    project = models.ForeignKey('Project',related_name='project_name',verbose_name='所属项目')
    provider = models.ForeignKey('Provider',related_name='provider_name',verbose_name='服务商')
    status = models.SmallIntegerField(choices=status_choices, default=0,verbose_name='状态')
    server_info = models.OneToOneField('Asset_Server',on_delete=models.CASCADE,verbose_name='关联信息')

    class Meta:
        permissions = (
            ("can_read_asset","读取资产"),
            ("can_change_asset","编辑资产"),
            ("can_add_asset","添加资产"),
            ("can_delete_asset","删除资产"),
        )
        ordering = ['-management_ip']
        verbose_name = '资产表'
        verbose_name_plural = "资产表"

    def __str__(self):
        return '<id:%s name:%s>' % (self.id, self.name)

class Asset_Server(models.Model):
    system_type_choices = (
        ('win','Windows'),
        ('lin','Centos'),
    )
    system_version_choices = (
        ('win08', 'Windows Server 2008'),
        ('win12', 'Windows Server 2012'),
        ('lin06', 'Centos 6'),
        ('lin07', 'Centos 7'),
    )
    ip_addr = models.GenericIPAddressField(unique=True,verbose_name='IP地址')
    hostname = models.CharField(max_length=100,verbose_name='主机名')
    username = models.CharField(max_length=100,blank=True,null=True,verbose_name='用户名')
    password = models.CharField(max_length=100,blank=True,null=True,verbose_name='密码')
    port = models.IntegerField(blank=True,null=True,verbose_name='远程端口')
    system_type = models.CharField(max_length=64, choices=system_type_choices, default='win', verbose_name='操作系统')
    system_version = models.CharField(max_length=64,choices=system_version_choices,default='win08',verbose_name='系统版本')
    cpu = models.SmallIntegerField(blank=True,null=True,verbose_name='CPU')
    disk = models.CharField(max_length=32,verbose_name='硬盘')
    memory = models.CharField(max_length=32, verbose_name='内存')

    class Meta:
        permissions = (
            ("can_read_server","读取服务器权限"),
            ("can_change_server","更改服务器权限"),
            ("can_add_server","添加服务器权限"),
            ("can_delete_server","删除服务器权限"),
        )
        verbose_name = "服务器表"
        verbose_name_plural = "服务器表"

    def __str__(self):
        return '%s' % self.ip_addr

class Project(models.Model):
    name = models.CharField(max_length=100,unique=True)
    class Meta:
        permissions = (
            ("can_read_project", "读取项目权限"),
            ("can_change_project", "更改服务器权限"),
            ("can_add_project", "添加服务器权限"),
            ("can_delete_project", "删除服务器权限"),
        )
        verbose_name = "项目表"
        verbose_name_plural = "项目表"
    def __str__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length=64,unique=True)

    class Meta:
        permissions = (
            ("can_read_location", "读取机房权限"),
            ("can_change_location", "更改机房权限"),
            ("can_add_location", "添加机房权限"),
            ("can_delete_location", "删除机房权限"),
        )
        verbose_name = '机房表'
        verbose_name_plural = "机房表"

    def __str__(self):
        return self.name

class Provider(models.Model):
    name = models.CharField(max_length=64,unique=True)
    deadline = models.TextField(unique=True)

    class Meta:
        permissions = (
            ("can_read_provider", "读取服务商权限"),
            ("can_change_provider", "更改服务商权限"),
            ("can_add_provider", "添加服务商权限"),
            ("can_delete_provider", "删除服务商权限"),
        )
        verbose_name = '服务商表'
        verbose_name_plural = "服务商表"

    def __str__(self):
        return self.name


