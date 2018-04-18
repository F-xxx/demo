from django.db import models

from userperm import custom_auth
from django.contrib.auth.models import Group,Permission
from django.utils.safestring import mark_safe
# Create your models here.


class Audit(models.Model):
    user = models.CharField(max_length=64)
    audit_time = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=32)
    action = models.CharField(max_length=64)
    action_ip = models.CharField(max_length=32)
    content = models.TextField()

    def __str__(self):
        return self.user

    class Meta:
        permissions = (
            ("can_read_audit","读取审计权限"),
            ("can_change_audit","更改审计权限"),
            ("can_add_audit","添加审计权限"),
            ("can_delete_audit","删除审计权限"),
        )
        ordering = ['-audit_time']

        verbose_name = '审计日志'
        verbose_name_plural = '审计日志'

class User_Profile(custom_auth.AbstractBaseUser,custom_auth.PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(
        verbose_name='staff status',
        default=True,
        help_text='Designates whether the user can log into this admin site.',
    )
    name = models.CharField(max_length=32)
    groups = models.ManyToManyField(Group, help_text=u'员工所属用户组')
    token = models.CharField('token', max_length=128, default=None, blank=True, null=True)
    # roles = models.ManyToManyField('Role', blank=True)
    department = models.CharField('部门', max_length=32, default=None, blank=True, null=True)
    tel = models.CharField('座机', max_length=32, default=None, blank=True, null=True)
    memo = models.TextField('备注', blank=True, null=True, default=None)
    date_joined = models.DateTimeField(blank=True, null=True, auto_now_add=True)

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['name','token','department','tel','mobile','memo']
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):  # __str__ on Python 2
        return self.email

    # def has_perm(self, perm, obj=None):
    #     "Does the user have a specific permission?"
    #     # Simplest possible answer: Yes, always
    #     return True
    def has_perms(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_superuser(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = "用户信息"
    objects = custom_auth.UserManager()
