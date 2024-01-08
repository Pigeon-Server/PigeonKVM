"""
URL configuration for ipkvm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

import app.apis.auth as auth
import app.apis.fileManager as fileManager
import app.apis.control as control
import app.apis.admin.users as users
import app.apis.admin.permission as permission
import app.apis.admin.auditAndLogger as auditAndLogger
import app.apis.userInfo as userInfo

urlpatterns = [
    # 登录
    path('auth/login', auth.AuthLogin),  # 登入（POST）
    path('auth/logout', auth.AuthOutLog),  # 登出（ALL）
    # 控制
    path('control/api/fastInput', control.fastInput),  # 快速键入(POST)
    path('control/api/buttonClick', control.clickButton),  # 点击按钮(POST)
    path('control/api/getLedStatus', control.getLedStatus),  # 获取LED状态(ALL)
    # 用户管理
    path('admin/api/getUserList', users.getUserList),  # 获取用户列表（ALL）
    path('admin/api/addUser', users.addUser),  # 新增用户（POST）
    path('admin/api/delUser', users.delUser),  # 删除用户（POST）
    path('admin/api/getUserPermission', users.getUserPermission),  # 获取用户权限（POST）
    path('admin/api/getUserInfo', users.getUserInfo),  # 获取用户信息（POST）
    path('admin/api/setUserInfo', users.setUserInfo),  # 设置用户信息（POST）
    # 权限管理
    path('admin/api/getPermissionGroups', permission.getPermissionGroupsList),  # 获取权限组列表（ALL）
    path('admin/api/getPermissionList', permission.getPermissionList),  # 获取权限列表（ALL）
    path('admin/api/addPermissionGroup', permission.addPermissionGroup),  # 新增权限组列表 （POST）
    path('admin/api/delPermissionGroup', permission.delPermissionGroup),  # 删除权限组 （POST）
    path('admin/api/getPermissionGroupInfo', permission.getPermissionGroupInfo),  # 获取权限组信息 （POST）
    path('admin/api/setPermissionGroup', permission.setPermissionGroup),  # 设置权限组 （POST）
    # 审计
    path('admin/api/auditAndLogger/audit', auditAndLogger.getAudit),  # 获取审计日志（POST）
    path('admin/api/auditAndLogger/accessLog', auditAndLogger.getAccessLog),  # 获取访问日志（POST）
    path('admin/api/auditAndLogger/fileChangeLog', auditAndLogger.getFileChangeLog),  # 获取文件日志（POST）
    path('admin/api/auditAndLogger/systemLog', auditAndLogger.getSystemLog),  # 获取系统日志（POST）
    # 个人信息编辑
    path("userInfo/api/getInfo", userInfo.getUserInfo),  # 获取个人信息（ALL）
    path("userInfo/api/editInfo", userInfo.setUserInfo),  # 修改个人信息（POST）
    path('userInfo/api/uploadAvatar', userInfo.uploadAvatar),  # 头像上传（POST）
    path('userInfo/api/getAvatar', userInfo.getAvatar),  # 获取头像（GET）
    path("userInfo/api/setPassword", userInfo.setPassword),  # 设置密码（POST）
    # 下载
    path('files/download/<token>', fileManager.temporary_link_download),  # 使用临时链接下载文件（GET）
    # 静态页面
    re_path('.*', TemplateView.as_view(template_name="index.html")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
