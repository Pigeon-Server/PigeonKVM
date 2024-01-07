from app.models import Users, Permission_groups, Settings
from app.util.DataBaseTools import getPageContent, getMaxPage, writeAccessLog, writeSystemLog, writeAudit
from app.util.Request import RequestLoadJson, getClientIp
from app.util.Response import ResponseJson
from app.util.logger import Log

import json


# 获取权限组列表
def getPermissionGroupsList(req):
    if req.method == "POST":
        try:
            req_json = RequestLoadJson(req)
        except Exception as e:
            Log.error(e)
            return ResponseJson({"status": -1, "msg": f"JSON解析失败:{e}"})
        else:
            PageContent = []
            page = req_json.get("page", 1)
            pageSize = req_json.get("pageSize", 20)
            search = req_json.get("search", "")
            result = Permission_groups.objects.filter(name__icontains=search if search else "")
            pageQuery = getPageContent(result, page if page > 0 else 1, pageSize)
            if pageQuery:
                for item in pageQuery:
                    PageContent.append({
                        "id": item.get("id"),
                        "name": item.get("name"),
                        "creator": Users.objects.filter(id=item.get("creator_id")).first().userName if item.get(
                            "creator_id") else None,
                        "createdAt": item.get("createdAt"),
                        "disable": item.get("disable")
                    })
            writeAccessLog(req.session.get("userID"), getClientIp(req), f"Get Permission Groups List(Search: {search} Page: {page} Page Size: {pageSize})")
            return ResponseJson({
                "status": 1,
                "data": {
                    "maxPage": getMaxPage(Permission_groups.objects.all().count(), 20),
                    "currentPage": page,
                    "PageContent": PageContent
                }
            })

    else:
        return ResponseJson({"status": -1, "msg": "请求方式不正确"})


# 新建权限组
def addPermissionGroup(req):
    if req.method == 'POST':
        try:
            req_json = RequestLoadJson(req)
        except Exception as e:
            Log.error(e)
            return ResponseJson({"status": -1, "msg": "JSON解析失败"})
        else:
            name = req_json.get("name")
            if Permission_groups.objects.filter(name=name):
                return ResponseJson({"status": 0, "msg": "组已存在"})
            creator = Users.objects.filter(id=req.session.get("userID")).first()
            disable = req_json.get("disable")
            permission = req_json.get("permissions")
            if name and creator and permission and disable is not None:
                allPermission = permission.get("all")
                viewDevice = permission.get("viewDevice")
                controllingDevice = permission.get("controllingDevice")
                changeDevicePowerState = permission.get("changeDevicePowerState")
                changeSettings = permission.get("changeSettings")
                manageUsers = permission.get("manageUsers")
                managePermissionGroups = permission.get("managePermissionGroups")
                viewAudit = permission.get("viewAudit")
                editAudit = permission.get("editAudit")

                Permission_groups.objects.create(
                    name=name,
                    creator=creator,
                    disable=disable,
                    all=allPermission,
                    viewDevice=viewDevice,
                    controllingDevice=controllingDevice,
                    changeDevicePowerState=changeDevicePowerState,
                    changeSettings=changeSettings,
                    manageUsers=manageUsers,
                    managePermissionGroups=managePermissionGroups,
                    viewAudit=viewAudit,
                    editAudit=editAudit
                )
                writeAudit(req.session.get("userID"), "Add Permission Group(添加权限组)", "Permission Manager(权限管理)", f"Name:{name} Permission: {permission} Disable: {disable}")
                return ResponseJson({"status": 1, "msg": "添加成功"})

            elif not creator:
                return ResponseJson({"status": -1, "msg": "未登录"})
            else:
                return ResponseJson({"status": -1, "msg": "参数不完整"})

    else:
        return ResponseJson({"status": -1, "msg": "请求方式不正确"})


# 删除权限组
def delPermissionGroup(req):
    if req.method == 'POST':
        try:
            req_json = RequestLoadJson(req)
        except Exception as e:
            Log.error(e)
            return ResponseJson({"status": -1, "msg": "JSON解析失败"})
        else:
            PermissionGroupId = req_json.get("id")
            if not PermissionGroupId:
                return ResponseJson({"status": -1, "msg": "参数不完整"})
            query = Permission_groups.objects.filter(id=PermissionGroupId).first()
            if query:
                writeAudit(req.session.get("userID"), "Del Permission Group(删除权限组)", "Permission Manager(权限管理)", query.name)
                query.delete()
                return ResponseJson({"status": 1, "msg": "组已删除"})
            else:
                return ResponseJson({"status": 0, "msg": "组不存在"})
    else:
        return ResponseJson({"status": -1, "msg": "请求方式不正确"})


# 获取权限组信息
@Log.catch
def getPermissionGroupInfo(req):
    if req.method == 'POST':
        try:
            req_json = RequestLoadJson(req)
        except Exception as e:
            Log.error(e)
            return ResponseJson({"status": -1, "msg": "JSON解析失败"})
        else:
            PermissionGroupId = req_json.get("id")
            if not PermissionGroupId:
                return ResponseJson({"status": -1, "msg": "参数不完整"})
            query = Permission_groups.objects.filter(id=PermissionGroupId).first()
            if query:
                writeAccessLog(req.session.get("userID"), getClientIp(req), f"Get Permission Group Info: {query.name}")
                return ResponseJson({"status": 1, "data": {
                    "id": query.id,
                    "name": query.name,
                    "creator": query.creator.userName if query.creator else None,
                    "createdAt": query.createdAt,
                    "disable": query.disable,
                    "Permission": {
                        "all": query.all,
                        "viewDevice": query.viewDevice,
                        "controllingDevice": query.controllingDevice,
                        "changeDevicePowerState": query.changeDevicePowerState,
                        "changeSettings": query.changeSettings,
                        "manageUsers": query.manageUsers,
                        "managePermissionGroups": query.managePermissionGroups,
                        "viewAudit": query.viewAudit,
                        "editAudit": query.editAudit
                    }
                }})
            else:
                return ResponseJson({"status": 0, "msg": "组不存在"})
    else:
        return ResponseJson({"status": -1, "msg": "请求方式不正确"})


# 修改权限组
def setPermissionGroup(req):
    if req.method == 'POST':
        try:
            req_json = RequestLoadJson(req)
        except Exception as e:
            Log.error(e)
            return ResponseJson({"status": -1, "msg": "JSON解析失败"})
        else:
            GroupId = req_json.get("id")
            data = req_json.get("data")
            if GroupId and data:
                Group = Permission_groups.objects.filter(id=GroupId).first()
                newName = data.get("newName")
                disable = data.get("disable")
                permissions = data.get("permissions")
                clientIp = getClientIp(req)
                userID = req.session.get("userID")

                if newName and newName != Group.name:
                    writeAudit(userID, "Rename Permission Group(重命名权限组)", "Permission Manager(权限管理)", f"{Group.name}-->{newName}")
                    Group.name = newName
                if disable != Group.disable:
                    writeAudit(userID, "Update Status Permission Group(更新权限组状态)", "Permission Manager(权限管理)",
                               f"{Group.name}: {Group.disable}-->{disable}")
                    Group.disable = disable

                if permissions:
                    Log.debug(permissions)
                    allPermission = permissions.get("all")
                    viewDevice = permissions.get("viewDevice")
                    controllingDevice = permissions.get("controllingDevice")
                    changeDevicePowerState = permissions.get("changeDevicePowerState")
                    changeSettings = permissions.get("changeSettings")
                    manageUsers = permissions.get("manageUsers")
                    managePermissionGroups = permissions.get("managePermissionGroups")
                    viewAudit = permissions.get("viewAudit")
                    editAudit = permissions.get("editAudit")
                    if allPermission is not None and allPermission != Group.all:
                        writeAudit(userID, "Edit Group Permissions(编辑组拥有的权限): all(全部)", "Permission Manager(权限管理)",
                                   f"{Group.name}: {Group.all}-->{allPermission}")
                        if allPermission:
                            writeSystemLog(2, "Add High-risk Permission Group: Create a new super admin group", Group.name)
                        Group.all = allPermission
                    if viewDevice is not None and viewDevice != Group.viewDevice:
                        writeAudit(userID, "Edit Group Permissions(编辑组拥有的权限): ViewDevice(浏览设备)",
                                   "Permission Manager(权限管理)",
                                   f"{Group.name}: {Group.viewDevice}-->{viewDevice}")
                        Group.viewDevice = viewDevice
                    if controllingDevice is not None and controllingDevice != Group.controllingDevice:
                        writeAudit(userID, "Edit Group Permissions(编辑组拥有的权限): ControllingDevice(控制设备)", "Permission Manager(权限管理)",
                                   f"{Group.name}: {Group.controllingDevice}-->{controllingDevice}")
                        Group.controllingDevice = controllingDevice
                    if changeDevicePowerState is not None and changeDevicePowerState != Group.changeDevicePowerState:
                        writeAudit(userID, "Edit Group Permissions(编辑组拥有的权限): ChangeDevicePowerState(改变设备电源状态)", "Permission Manager(权限管理)",
                                   f"{Group.name}: {Group.changeDevicePowerState}-->{changeDevicePowerState}")
                        Group.changeDevicePowerState = changeDevicePowerState
                    if changeSettings is not None and changeSettings != Group.changeSettings:
                        writeAudit(userID, "Edit Group Permissions(编辑组拥有的权限): ChangeSettings(更改设置)", "Permission Manager(权限管理)",
                                   f"{Group.name}: {Group.changeSettings}-->{changeSettings}")
                        Group.changeSettings = changeSettings
                    if manageUsers is not None and manageUsers != Group.manageUsers:
                        writeAudit(userID, "Edit Group Permissions(编辑组拥有的权限): ManageUsers(管理用户)", "Permission Manager(权限管理)",
                                   f"{Group.name}: {Group.manageUsers}-->{manageUsers}")
                        if manageUsers:
                            writeSystemLog(2, "Add High-risk Permission Group: Manageable users", Group.name)
                        Group.manageUsers = manageUsers
                    if managePermissionGroups is not None and managePermissionGroups != Group.managePermissionGroups:
                        writeAudit(userID, "Edit Group Permissions(编辑组拥有的权限): ManagePermissionGroups(管理权限组)", "Permission Manager(权限管理)",
                                   f"{Group.name}: {Group.managePermissionGroups}-->{managePermissionGroups}")
                        if managePermissionGroups:
                            writeSystemLog(2, "Add High-risk Permission Group: Permission groups can be modified", Group.name)
                        Group.managePermissionGroups = managePermissionGroups
                    if viewAudit is not None and viewAudit != Group.viewAudit:
                        writeAudit(userID, "Edit Group Permissions(编辑组拥有的权限): ViewAudit(浏览审计内容)", "Permission Manager(权限管理)",
                                   f"{Group.name}: {Group.viewAudit}-->{viewAudit}")
                        Group.viewAudit = viewAudit
                    if editAudit is not None and editAudit != Group.editAudit:
                        writeAudit(userID, "Edit Group Permissions(编辑组拥有的权限): EditAudit(编辑审计内容)", "Permission Manager(权限管理)",
                                   f"{Group.name}: {Group.editAudit}-->{editAudit}")
                        if editAudit:
                            writeSystemLog(2, "Add High-risk Permission Group: Clear the audit", Group.name)
                        Group.editAudit = editAudit
                Group.save()
                return ResponseJson({"status": 1, "msg": "成功", "data": {
                    "id": Group.id,
                    "name": Group.name,
                    "Permission": {
                        "all": Group.all,
                        "viewDevice": Group.viewDevice,
                        "controllingDevice": Group.controllingDevice,
                        "changeDevicePowerState": Group.changeDevicePowerState,
                        "changeSettings": Group.changeSettings,
                        "manageUsers": Group.manageUsers,
                        "managePermissionGroups": Group.managePermissionGroups,
                        "viewAudit": Group.viewAudit,
                        "editAudit": Group.editAudit
                    }
                }})
            else:
                return ResponseJson({"status": -1, "msg": "参数不完整"})
    else:
        return ResponseJson({"status": -1, "msg": "请求方式不正确"})


def getPermissionList(req):
    translate = json.loads(Settings.objects.filter(Settings="PermissionTranslate").first().value)

    def getTranslate(name):
        return translate.get(name) if translate.get(name) else name

    writeAccessLog(req.session.get("userID"), getClientIp(req), f"Get Permission List")
    return ResponseJson({
        "status": 1,
        "msg": "成功",
        "data": {
            "all": getTranslate("all"),
            "viewDevice": getTranslate("viewDevice"),
            "controllingDevice": getTranslate("controllingDevice"),
            "changeDevicePowerState": getTranslate("changeDevicePowerState"),
            "changeSettings": getTranslate("changeSettings"),
            "manageUsers": getTranslate("manageUsers"),
            "managePermissionGroups": getTranslate("managePermissionGroups"),
            "viewAudit": getTranslate("viewAudit"),
            "editAudit": getTranslate("editAudit")
        }
    })
