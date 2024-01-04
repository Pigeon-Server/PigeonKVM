from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, redirect
from app.models import Users, Permission_groups

class PermissionsMiddleware(MiddlewareMixin):
    """
    权限校验中间件
    """
    def process_request(self, request):
        userId = request.session.get("userId")
        user = Users.objects.filter(id=userId).first()
        permission = Permission_groups.objects.filter(id=user.permission_id).first()

        # accessiblePages = {
        #     "viewDevice": [],
        #     "controllingDevice": [],
        #     "changeDevicePowerState": []
        # }

        """
            all = models.BooleanField("所有权限", default=False, null=True)
            viewDevice = models.BooleanField("查看设备", default=False, null=True)
            controllingDevice = models.BooleanField("控制设备", default=False, null=True)
            changeDevicePowerState = models.BooleanField("开关机", default=False, null=True)
            changeSettings = models.BooleanField("更改设置", default=False, null=True)
            manageUsers = models.BooleanField("管理用户", default=False, null=True)
            managePermissionGroups = models.BooleanField("管理权限组", default=False, null=True)
            viewAudit = models.BooleanField("查看审计内容", default=False, null=True)
            editAudit = models.BooleanField("编辑审计", default=False, null=True)
        """

        # 页面权限表
        accessPermission = {
            "page": {
                "/admin/users": "manageUsers",
                "/admin/permission": "managePermissionGroups",
                "/admin/audit": "viewAudit",
                "/admin/settings": "changeSettings",
            },
            "api": {
                "/admin/api/getUserList": "manageUsers",
                "/admin/api/addUser": "manageUsers",
                "/admin/api/delUser": "manageUsers",
                "/admin/api/getUserPermission": "manageUsers",
                "/admin/api/getUserInfo": "manageUsers",
                "/admin/api/setUserInfo": "manageUsers",

                "/admin/api/getPermissionGroups": "managePermissionGroups",
                "/admin/api/getPermissionList": "managePermissionGroups",
                "/admin/api/addPermissionGroup": "managePermissionGroups",
                "/admin/api/delPermissionGroup": "managePermissionGroups",
                "/admin/api/getPermissionGroupInfo": "managePermissionGroups",
                "/admin/api/setPermissionGroup": "managePermissionGroups",

                "/admin/api/auditAndLogger/audit": "viewAudit",
                "/admin/api/auditAndLogger/accessLog": "viewAudit",
                "/admin/api/auditAndLogger/fileChangeLog": "viewAudit",
                "/admin/api/auditAndLogger/systemLog": "viewAudit",
            }
        }

        # 忽略权限
        Ignore = [
            "/login",
            "/auth/login",
            "/about",
            "/userInfo",
            "/userInfo/api/getInfo",
            "/userInfo/api/editInfo",
            "/userInfo/api/uploadAvatar",
            "/userInfo/api/getAvatar",
            "/userInfo/api/setPassword",
            "/files/download",
        ]

        # 忽略权限过滤器
        if request.path_info in Ignore:
            return

        if not permission:
            pass
        elif permission.disable:
            pass

        # if request.path_info in ["/login", "/auth/login"]:
        #     return
        # if request.session.get("user"):
        #     return
        # else:
        #     return redirect("/login")
