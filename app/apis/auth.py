import datetime

from app.util.Response import ResponseJson
from app.util.Request import RequestLoadJson, getClientIp
from app.util.PasswordTools import PasswordToMd5
from app.util.logger import Log
import app.util.Config as Config
from app.util.DataBaseTools import writeAudit

from app.models import Users, Permission_groups


# 登录
def AuthLogin(req):
    if req.method == 'POST':
        try:
            req_json = RequestLoadJson(req)
            Log.debug(req_json)
        except Exception as err:
            Log.error(err)
            return ResponseJson({"status": -1, "msg": "Json解析失败"})
        else:
            user = req_json.get("username")
            password = PasswordToMd5(req_json.get("password"))
            user = Users.objects.filter(userName=user, password=password).first()
            if user:
                if not user.disable:
                    req.session["user"] = user.userName
                    req.session["userID"] = user.id
                    req.session.set_expiry(int(Config.main_config.get("main").get("sessionExpiry")) * 60)
                    Log.info(f"用户{user.userName}已登陆")
                    user.lastLoginIP = getClientIp(req)
                    user.lastLoginTime = datetime.datetime.now()
                    user.save()
                    writeAudit(user.id, "Login", "Auth", user.lastLoginIP)
                    group = Permission_groups.objects.filter(id=user.permission_id).first() if user.permission_id is not None else None
                    return ResponseJson({
                        "status": 1,
                        "msg": "登录成功",
                        "data": {
                            "id": user.id,
                            "userName": user.userName,
                            "realName": user.realName,
                            "email": user.email,
                            "group": group.name if group else None,
                            "permissions": {
                                "all": group.all if group else False,
                                "viewDevice": group.viewDevice if group else False,
                                "controllingDevice": group.controllingDevice if group else False,
                                "changeDevicePowerState": group.changeDevicePowerState if group else False,
                                "changeSettings": group.changeSettings if group else False,
                                "manageUsers": group.manageUsers if group else False,
                                "managePermissionGroups": group.managePermissionGroups if group else False,
                                "viewAudit": group.viewAudit if group else False,
                                "editAudit": group.editAudit if group else False
                            }
                        }
                    })
                else:
                    return ResponseJson({"status": 0, "msg": "账户被禁用，请联系管理员"})
            else:
                return ResponseJson({"status": 0, "msg": "用户名或密码错误"})
    else:
        return ResponseJson({"status": -1, "msg": "请求方法不正确"})


# 登出
def AuthOutLog(req):
    if req.session.get("user"):
        user = req.session.get("user")
        # Log.debug(req.session.get("userID"))
        # writeAudit(req.session.get("userID"), "Outlog", "Auth", getClientIp(req))
        req.session.clear()
        Log.info(f"用户{user}已登出")
        return ResponseJson({"status": 1, "msg": "登出成功"})
    else:
        return ResponseJson({"status": 0, "msg": "您未登录"})
