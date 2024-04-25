from app.models import Users, Permission_groups, Settings
from app.util.DataBaseTools import getPageContent, getMaxPage, writeAccessLog, writeSystemLog, writeAudit
from app.util.Request import RequestLoadJson, getClientIp
from app.util.Response import ResponseJson
from app.util.logger import Log
from app.util.permission import *

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
                        "creator": Users.objects.filter(id=item.get("creator_id")).first().userName if item.get("creator_id") else None,
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
                group = Permission_groups.objects.create(
                    name=name,
                    creator=creator,
                    disable=disable
                )
                groupPermission(group.id).update_permissions_list(permission)
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
                if Users.objects.filter(permission=query):
                    return ResponseJson({"status": 2, "msg": "当前组正在使用中，无法删除"})
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
                    "Permission": groupPermission(query.id).get_permissions_dict()
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
                newName: str = data.get("newName")
                disable: bool = data.get("disable")
                permissions: list = data.get("permissions")
                clientIp: str = getClientIp(req)
                userID: int = req.session.get("userID")

                if newName and newName != Group.name:
                    writeAudit(
                        userID,
                        "Rename Permission Group(重命名权限组)",
                        "Permission Manager(权限管理)",
                        f"{Group.name}-->{newName}"
                    )
                    Group.name = newName
                if disable != Group.disable:
                    writeAudit(
                        userID,
                        "Update Status Permission Group(更新权限组状态)",
                        "Permission Manager(权限管理)",
                        f"{Group.name}: {Group.disable}-->{disable}")
                    Group.disable = disable

                if permissions:
                    groupPermission(Group.id).update_permissions_list(permissions)

                Group.save()
                return ResponseJson({"status": 1, "msg": "成功", "data": {
                    "id": Group.id,
                    "name": Group.name,
                    "Permission": groupPermission(Group.id).get_permissions_dict()
                }})
            else:
                return ResponseJson({"status": -1, "msg": "参数不完整"})
    else:
        return ResponseJson({"status": -1, "msg": "请求方式不正确"})


def getPermissionList(req):
    writeAccessLog(req.session.get("userID"), getClientIp(req), f"Get Permission List")
    data: dict = {}
    for permission in get_all_permission_item_info():
        data.update({permission['permission']: permission['translate']})

    return ResponseJson({
        "status": 1,
        "msg": "成功",
        "data": data
    })
