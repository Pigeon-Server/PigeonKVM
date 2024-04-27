from enum import Enum

from django.db import models
from django.utils import timezone
import uuid
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ipkvm.settings")
# django.setup()


# Create your models here.

# 用户列表
class Users(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    userName = models.CharField("用户名", max_length=32, unique=True)
    realName = models.CharField("姓名", max_length=32, unique=True, null=True)
    email = models.EmailField("电子邮箱", max_length=100, unique=True, null=True)
    createdAt = models.DateTimeField("创建时间", null=True, auto_now_add=True)
    lastLoginTime = models.DateTimeField("上次登录时间", null=True, auto_now=True)
    lastLoginIP = models.GenericIPAddressField("上次登录IP", null=True)
    password = models.CharField("密码(md5)", max_length=128)
    avatar = models.CharField("头像hash", max_length=64, null=True)
    permission = models.ForeignKey("Permission_groups", on_delete=models.DO_NOTHING, null=True)
    disable = models.BooleanField("是否禁用", default=False, null=True)


class Permission_groups(models.Model):
    """权限组列表"""
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField("权限组名", max_length=30, unique=True)
    creator = models.ForeignKey("Users", on_delete=models.DO_NOTHING, null=True)
    createdAt = models.DateTimeField("创建时间", auto_now_add=True)
    permissions = models.ManyToManyField('Permission_Item', related_name='groups')
    disable = models.BooleanField("是否禁用", null=True)


class Permission_Item(models.Model):
    """权限列表"""
    id = models.AutoField("权限项ID", primary_key=True, unique=True)
    permission = models.CharField("权限名", max_length=30, unique=True)
    description = models.CharField("权限项介绍", max_length=100, null=True)
    translate = models.CharField("权限翻译", max_length=30, unique=True, null=True)


# 审计
class Audit(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    user = models.ForeignKey("Users", on_delete=models.DO_NOTHING)
    time = models.DateTimeField("发生时间", auto_now_add=True)
    action = models.CharField("动作", max_length=256)
    module = models.CharField("模块", max_length=256)
    content = models.CharField("数据", max_length=4096)


# 系统日志
class System_Log(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    time = models.DateTimeField("发生时间", auto_now_add=True)
    level = models.IntegerField("日志等级")
    module = models.CharField("模块", max_length=256)
    content = models.CharField("日志内容", max_length=1024)


# 访问日志
class Access_Log(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    user = models.ForeignKey("Users", on_delete=models.DO_NOTHING)
    ip = models.GenericIPAddressField("IP地址", null=True)
    time = models.DateTimeField("操作时间", auto_now_add=True)
    module = models.CharField("访问的模块", max_length=512)


# 文件修改日志
class FileChange_Log(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    user = models.ForeignKey("Users", db_column="用户", on_delete=models.DO_NOTHING)
    time = models.DateTimeField("操作时间", auto_now_add=True)
    action = models.CharField("动作", max_length=512)
    filepath = models.CharField("目标文件", max_length=4096)


# 临时下载链接
class Temporary_link(models.Model):
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    userID = models.ForeignKey("Users", on_delete=models.DO_NOTHING)
    filePath = models.CharField("文件路径", max_length=255)  # 文件路径
    createdAt = models.DateTimeField("链接创建时间", auto_now_add=True)
    used = models.BooleanField(default=False)
