from django.db import models
from django.utils import timezone
import uuid
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ipkvm.settings")
django.setup()

# Create your models here.

class Users(models.Model):
    """用户列表"""
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
    """权限组"""
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField("权限组名", max_length=30, unique=True)
    creator = models.ForeignKey("Users", on_delete=models.DO_NOTHING, null=True)
    createdAt = models.DateTimeField("创建时间", auto_now_add=True)
    all = models.BooleanField("所有权限", default=False, null=True)
    viewDevice = models.BooleanField("查看设备", default=False, null=True)
    controllingDevice = models.BooleanField("控制设备", default=False, null=True)
    changeDevicePowerState = models.BooleanField("开关机", default=False, null=True)
    changeSettings = models.BooleanField("更改设置", default=False, null=True)
    manageUsers = models.BooleanField("管理用户", default=False, null=True)
    managePermissionGroups = models.BooleanField("管理权限组", default=False, null=True)
    viewAudit = models.BooleanField("查看审计内容", default=False, null=True)
    editAudit = models.BooleanField("编辑审计", default=False, null=True)
    disable = models.BooleanField("是否禁用", default=False, null=True)


class GPIO(models.Model):
    """GPIO列表"""
    id = models.AutoField(primary_key=True, unique=True)
    Power_LED = models.IntegerField("电源灯GPIO号", unique=True, null=False)
    HDD_LED = models.IntegerField("硬盘灯GPIO号", unique=True, null=False)
    Power_Btn = models.IntegerField("电源键GPIO号", unique=True, null=False)
    Restart_Btn = models.IntegerField("重启按键GPIO号", unique=True, null=False)
    UsbDisk_EN = models.IntegerField("启用切换器GPIO号", unique=True, null=False)
    UsbDisk_Switch = models.IntegerField("USB切换GPIO号", unique=True, null=False)


class HID(models.Model):
    """HID设备"""
    id = models.AutoField(primary_key=True, unique=True)
    device = models.CharField("串口设备", max_length=60, null=False)
    baudrate = models.IntegerField("串口波特率", null=False)


class Video(models.Model):
    """视频设备"""
    id = models.AutoField(primary_key=True, unique=True)
    device = models.CharField("视频设备", max_length=60, null=False)
    width = models.IntegerField("视频宽度", null=False)
    height = models.IntegerField("视频高度", null=False)
    fps = models.IntegerField("视频帧率", null=False)


class Machine_Config(models.Model):
    """机器配置"""
    id = models.AutoField(primary_key=True, unique=True)
    enableMouse = models.BooleanField("启用鼠标", null=True)
    enableKeyboard = models.BooleanField("启用键盘", null=True)


class Machine_Group(models.Model):
    """设备组"""
    id = models.AutoField("组id", primary_key=True, unique=True)
    name = models.CharField("组名", max_length=30, null=False, unique=True)


class Machine(models.Model):
    """设备列表"""
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField("设备名", max_length=30)
    introduce = models.CharField("设备介绍", max_length=200, null=True)
    video = models.ForeignKey("Video", on_delete=models.DO_NOTHING)
    HID = models.ForeignKey("HID", on_delete=models.DO_NOTHING)
    GPIO = models.ForeignKey("GPIO", on_delete=models.DO_NOTHING)
    config = models.ForeignKey("Machine_Config", on_delete=models.DO_NOTHING)
    group = models.ForeignKey("Machine_Group", on_delete=models.DO_NOTHING)
    snapshot = models.FilePathField("服务器上次操作快照", null=True)


class Audit(models.Model):
    """审计"""
    id = models.AutoField(primary_key=True, unique=True)
    user = models.ForeignKey("Users", on_delete=models.DO_NOTHING)
    time = models.DateTimeField("发生时间", auto_now_add=True)
    action = models.CharField("动作", max_length=256)
    module = models.CharField("模块", max_length=256)
    content = models.CharField("数据", max_length=4096)


class System_Log(models.Model):
    """系统日志"""
    id = models.AutoField(primary_key=True, unique=True)
    time = models.DateTimeField("发生时间", auto_now_add=True)
    level = models.IntegerField("日志等级")
    module = models.CharField("模块", max_length=256)
    content = models.CharField("日志内容", max_length=1024)


class Access_Log(models.Model):
    """访问日志"""
    id = models.AutoField(primary_key=True, unique=True)
    user = models.ForeignKey("Users", on_delete=models.DO_NOTHING)
    ip = models.GenericIPAddressField("IP地址", null=True)
    time = models.DateTimeField("操作时间", auto_now_add=True)
    module = models.CharField("访问的模块", max_length=512, unique=True)


class FileChange_Log(models.Model):
    """文件修改日志"""
    id = models.AutoField(primary_key=True, unique=True)
    user = models.ForeignKey("Users", db_column="用户", on_delete=models.DO_NOTHING)
    time = models.DateTimeField("操作时间", auto_now_add=True)
    action = models.CharField("动作", max_length=512)
    filepath = models.CharField("目标文件", max_length=4096)


class Settings(models.Model):
    """系统设置"""
    id = models.AutoField(primary_key=True, unique=True)
    Settings = models.CharField("设置项名", max_length=120, unique=True)
    value = models.CharField("值", max_length=4096)
    lastModifiedTime = models.DateTimeField("上次修改时间", null=True, auto_now=True)
    lastModifiedUser = models.ForeignKey("Users", on_delete=models.DO_NOTHING, null=True)


class Temporary_link(models.Model):
    """临时链接"""
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    userID = models.ForeignKey("Users", on_delete=models.DO_NOTHING)
    filePath = models.CharField("文件路径", max_length=255)  # 文件路径
    createdAt = models.DateTimeField("链接创建时间", auto_now_add=True)
    used = models.BooleanField(default=False)
