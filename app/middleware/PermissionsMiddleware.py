from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, redirect
from app.models import Users, Permission_groups
from app.util.Response import ResponseJson

class PermissionsMiddleware(MiddlewareMixin):
    """
    权限校验中间件
    """
    def process_request(self, request):
        userId = request.session.get("userID")
        path_info = request.path_info

        # 忽略权限
        Ignore = [
            "/login",
            "/auth/login",
            "/error/403"
        ]

        # 页面权限表
        accessPermission = {
            "page": {
                "/admin/users": "manageUsers",
                "/admin/permission": "managePermissionGroups",
                "/admin/audit": "viewAudit",
                "/admin/settings": "changeSettings",
            },
            "api": {
                "/control/api/fastInput": "controllingDevice",
                "/control/api/buttonClick": "changeDevicePowerState",
                "/control/api/getLedStatus": "viewDevice",

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

        # 忽略权限过滤器
        if path_info in Ignore:
            return

        permission = Permission_groups.objects.filter(id=Users.objects.filter(id=userId).first().permission_id).values()[0]

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

        # 无权限时
        if not permission:
            if path_info in accessPermission.get("api").keys():
                return ResponseJson({"status": -1, "msg": "未授权访问-账户无权限"})
            elif path_info in accessPermission.get("page").keys():
                return redirect("/error/403")

        # 权限组被禁用时
        if permission.get("disable"):
            if path_info in accessPermission.get("api").keys():
                return ResponseJson({"status": -1, "msg": "未授权访问-组已禁用"})
            elif path_info in accessPermission.get("page").keys():
                return redirect("/error/403")

        # 拥有全部权限时
        if permission.get("all"):
            return

        # 检查API权限
        if path_info in accessPermission.get("api").keys():
            required = accessPermission.get("api").get(path_info)

            if required:
                if permission.get(required):
                    return
                else:
                    return ResponseJson({"status": -1, "msg": "未授权访问-无权限访问该API"})

        # 检查页面权限
        elif path_info in accessPermission.get("page").keys():
            required = accessPermission.get("page").get(path_info)
            if required:
                if required and permission.get(required):
                    return
                else:
                    return redirect("/error/403")

        # if request.path_info in ["/login", "/auth/login"]:
        #     return
        # if request.session.get("user"):
        #     return
        # else:
        #     return redirect("/login")
