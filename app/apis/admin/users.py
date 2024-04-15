import re

from app.models import Users, Permission_groups
from app.util.DataBaseTools import getMaxPage, getPageContent, writeAccessLog, writeAudit
from app.util.Response import ResponseJson
from app.util.Request import RequestLoadJson, getClientIp
from app.util.logger import Log
from app.util.PasswordTools import PasswordToMd5


# 获取用户列表
@Log.catch
def getUserList(req):
    if req.method == 'POST':
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
            result = Users.objects.filter(userName__icontains=search if search else "")
            pageQuery = getPageContent(result, page if page > 0 else 1, pageSize)
            maxPage = getMaxPage(result.count(), pageSize)
            if pageQuery:
                for item in pageQuery:
                    PageContent.append({
                        "id": item.get("id"),
                        "userName": item.get("userName"),
                        "realName": item.get("realName"),
                        "email": item.get("email"),
                        "createdAt": item.get("createdAt"),
                        "lastLoginTime": item.get("lastLoginTime"),
                        "lastLoginIP": item.get("lastLoginIP"),
                        "permissionGroupID": item.get("permission_id"),
                        "permissionGroupName": Permission_groups.objects.filter(id=item.get("permission_id")).first().name if item.get("permission_id") else None,
                        "disable": item.get("disable")
                    })
            writeAccessLog(req.session.get("userID"), getClientIp(req), f"Get User List(Search: {search} Page: {page} Page Size: {pageSize})")
            return ResponseJson({
                "status": 1,
                "data": {
                    "maxPage": maxPage,
                    "currentPage": page if page < maxPage else maxPage,
                    "PageContent": PageContent
                }
            })
    else:
        return ResponseJson({"status": -1, "msg": "请求方式不正确"})

# 新增用户
@Log.catch
def addUser(req):
    if req.method == 'POST':
        try:
            req_json = RequestLoadJson(req)
            Log.debug(req_json)
        except Exception as e:
            Log.error(e)
            return ResponseJson({"status": -1, "msg": f"JSON解析失败:{e}"})
        else:
            userName = req_json.get("userName")
            realName = req_json.get("realName")
            email = req_json.get("email")
            password = req_json.get("password")
            disable = req_json.get("disable")
            permission = req_json.get("permission")
            if userName and password:
                if Users.objects.filter(userName=userName):
                    return ResponseJson({"status": 0, "msg": "用户已存在"})
                if realName and Users.objects.filter(realName=realName):
                    return ResponseJson({"status": 0, "msg": "该用户已有账户"})
                if email and Users.objects.filter(email=email):
                    return ResponseJson({"status": 0, "msg": "邮箱已使用过"})
                if not re.match("^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[^\w\s]).{6,16}", password):
                    return ResponseJson({"status": 0, "msg": "密码不符合安全要求（至少6字符，必须含有数字，小写字母，大写字母，特殊字符）"})
                createUser = Users.objects.create(
                    userName=userName,
                    realName=realName,
                    email=email,
                    password=password,
                    disable=disable,
                    permission=Permission_groups.objects.get(id=permission) if permission else None
                )
                if createUser:
                    writeAudit(req.session.get("userID"), "Add User(添加用户)",
                               "User Manager(用户管理)",
                               f"User Name:{userName} Real Name: {realName} Email: {email} Disable: {disable}")
                    return ResponseJson({"status": 1, "msg": "用户添加成功"})
                else:
                    return ResponseJson({"status": 0, "msg": "用户添加失败"})
            else:
                return ResponseJson({"status": -1, "msg": "参数不完整"})
    else:
        return ResponseJson({"status": -1, "msg": "请求方式不正确"})


# 删除用户
@Log.catch
def delUser(req):
    if req.method == 'POST':
        try:
            req_json = RequestLoadJson(req)
        except Exception as e:
            Log.error(e)
            return ResponseJson({"status": -1, "msg": f"JSON解析失败:{e}"})
        else:
            userId = req_json.get("id")
            Log.debug(userId)
            Log.debug(userId == req.session.get("userID"))
            if not userId:
                return ResponseJson({"status": -1, "msg": "参数不完整"})
            if userId == req.session.get("userID"):
                ResponseJson({"status": 0, "msg": "不能删除当前登录用户"})
            query = Users.objects.filter(id=userId).first()
            if query.permission_id and Permission_groups.objects.filter(id=query.permission_id).first().all:
                ResponseJson({"status": 0, "msg": "不能删除拥有All权限的用户"})
            if query:
                writeAudit(req.session.get("userID"), "Del User(删除用户)",
                           "User Manager(用户管理)",
                           f"User Id: {query.id} User Name: {query.userName}")
                query.delete()
                return ResponseJson({"status": 1, "msg": "用户已删除"})
            else:
                return ResponseJson({"status": 0, "msg": "用户不存在"})
    else:
        return ResponseJson({"status": -1, "msg": "请求方式不正确"})


# 获取用户权限
@Log.catch
def getUserPermission(req):
    if req.method == 'POST':
        try:
            req_json = RequestLoadJson(req)
        except Exception as e:
            Log.error(e)
            return ResponseJson({"status": -1, "msg": f"JSON解析失败:{e}"})
        else:
            userId = req_json.get("id")
            if not userId:
                return ResponseJson({"status": -1, "msg": "参数不完整"})
            query = Users.objects.filter(id=userId).first()
            if query:
                writeAccessLog(req.session.get("userID"), getClientIp(req),f"Get User Permission(User ID: {userId})")
                return ResponseJson({"status": 1, "data": {
                    "permissionId": query.permission_id,
                    "permissionName": Permission_groups.objects.filter(id=query.permission_id).first().name if query.permission_id else None,
                }})
            else:
                return ResponseJson({"status": 0, "msg": "用户不存在"})
    else:
        return ResponseJson({"status": -1, "msg": "请求方式不正确"})


# 获取用户信息
@Log.catch
def getUserInfo(req):
    if req.method == 'POST':
        try:
            req_json = RequestLoadJson(req)
        except Exception as e:
            Log.error(e)
            return ResponseJson({"status": -1, "msg": f"JSON解析失败:{e}"})
        else:
            userId = req_json.get("id")
            if not userId:
                return ResponseJson({"status": -1, "msg": "参数不完整"})
            query = Users.objects.filter(id=userId).first()
            if query:
                writeAccessLog(req.session.get("userID"), getClientIp(req), f"Get User Info(User ID: {userId})")
                return ResponseJson({"status": 1, "data": {
                    "id": query.id,
                    "userName": query.userName,
                    "realName": query.realName,
                    "email": query.email,
                    "permissionId": query.permission_id,
                    "permissionName": Permission_groups.objects.filter(id=query.permission_id).first().name if query.permission_id else None,
                    "disable": query.disable
                }})
            else:
                return ResponseJson({"status": 0, "msg": "用户不存在"})
    else:
        return ResponseJson({"status": -1, "msg": "请求方式不正确"})


# 修改用户信息
@Log.catch
def setUserInfo(req):
    if req.method == 'POST':
        try:
            req_json = RequestLoadJson(req)
            Log.debug(req_json)
        except Exception as e:
            Log.error(e)
            return ResponseJson({"status": -1, "msg": f"JSON解析失败:{e}"})
        else:
            userId = req_json.get("id")
            data = req_json.get("data")
            if userId and data:
                User = Users.objects.filter(id=userId).first()
                userName = data.get("userName")
                realName = data.get("realName")
                email = data.get("email")
                password = data.get("password")
                permission = data.get("permission")
                disable = data.get("disable") if isinstance(data.get("disable"), bool) else bool(data.get("disable"))
                if userName and userName != User.userName:
                    if Users.objects.filter(userName=userName):
                        return ResponseJson({"status": 0, "msg": "用户已存在"})
                    writeAudit(req.session.get("userID"), "Edit User Info(编辑用户): Update UserName(更新用户名)",
                               "User Manager(权限管理)",
                               f"{User.userName}-->{userName}")
                    User.userName = userName
                if realName and realName != User.realName:
                    if Users.objects.filter(realName=realName):
                        return ResponseJson({"status": 0, "msg": "用户已存在"})
                    writeAudit(req.session.get("userID"), "Edit User Info(编辑用户): Update RealName(更新真实姓名)",
                               "User Manager(用户管理)",
                               f"{User.realName}-->{realName}")
                    User.realName = realName
                if email and email != User.email:
                    if Users.objects.filter(email=email):
                        return ResponseJson({"status": 0, "msg": "邮箱已使用"})
                    writeAudit(req.session.get("userID"), "Edit User Info(编辑用户): Update RealName(更新邮箱)",
                               "User Manager(用户管理)",
                               f"{User.email}-->{email}")
                    User.email = email
                if password and password != User.password:
                    if not re.match("^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[^\w\s]).{6,16}", password):
                        return ResponseJson({"status": 0, "msg": "密码不符合安全要求（至少6字符，必须含有数字，小写字母，大写字母，特殊字符）"})
                    writeAudit(req.session.get("userID"), "Edit User Info(编辑用户): Update RealName(更新密码)",
                               "User Manager(用户管理)",
                               PasswordToMd5(password))
                    User.password = PasswordToMd5(password)
                if permission and permission != User.permission_id:
                    if Permission_groups.objects.filter(id=permission):
                        newPermission = Permission_groups.objects.filter(id=permission).first()
                        writeAudit(req.session.get("userID"), "Edit User Info(编辑用户): Update Permission Group(更新权限组)",
                                   "User Manager(权限管理)",
                                   f"{Permission_groups.objects.filter(id=User.permission_id).first().name if User.permission_id else 'None'}-->{newPermission.name}")
                        User.permission_id = newPermission
                    else:
                        return ResponseJson({"status": 0, "msg": "所选择的权限组不存在"})
                if disable and disable != User.disable:
                    writeAudit(req.session.get("userID"), "Edit User Info(编辑用户): Edit Status(更新用户状态)",
                               "User Manager(权限管理)",
                               f"{not User.disable}-->{not disable}")
                    User.disable = disable
                User.save()
                return ResponseJson({"status": 1, "msg": "成功", "data": {
                    "id": User.id,
                    "userName": User.userName,
                    "realName": User.realName,
                    "email": User.email,
                    "permissionId": User.permission_id.id if isinstance(User.permission_id, Permission_groups) else User.permission_id,
                    "permissionName": Permission_groups.objects.filter(id=User.permission_id.id if isinstance(User.permission_id, Permission_groups) else User.permission_id).first().name if User.permission_id else None,
                    "disable": User.disable
                }})
            else:
                return ResponseJson({"status": -1, "msg": "参数不完整"})
    else:
        return ResponseJson({"status": -1, "msg": "请求方式不正确"})