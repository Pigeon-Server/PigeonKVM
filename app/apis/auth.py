import datetime

from app.util.Response import ResponseJson
from app.util.Request import RequestLoadJson, getClientIp
from app.util.PasswordTools import PasswordToMd5
from app.util.logger import Log
import app.util.Config as Config
from app.util.DataBaseTools import writeAudit

from app.models import Users


# 登录
def AuthLogin(req):
    if req.session.get("user"):
        return ResponseJson({"status": 1, "msg": "当前账户已登录"})
    if req.method == 'POST':
        req_json = RequestLoadJson(req)
        user = req_json.get("username")
        password = PasswordToMd5(req_json.get("password"))
        user = Users.objects.filter(userName=user, password=password).first()
        if user:
            if not user.disable:
                req.session["user"] = user.userName
                req.session["userID"] = user.id
                req.session.set_expiry(int(Config.main_config.get("main").get("sessionExpiry")) * 60)
                Log.success(f"用户[{user.userName}]已登陆")
                user.lastLoginIP = getClientIp(req)
                user.lastLoginTime = datetime.datetime.now()
                user.save()
                writeAudit(user.id, "Login", "Auth", user.lastLoginIP)
                return ResponseJson({"status": 1, "msg": "登录成功"})
            else:
                return ResponseJson({"status": 0, "msg": "账户被禁用，请联系管理员"})
        else:
            return ResponseJson({"status": 0, "msg": "用户名或密码错误"})
    else:
        return ResponseJson({"status": -1, "msg": "请求方法不正确"})


# 登出
def AuthOutLog(req):
    if req.session.get("user"):
        writeAudit(req.session.get("userID"), "Outlog", "Auth", getClientIp(req))
        req.session.clear()
        return ResponseJson({"status": 1, "msg": "登出成功"})
    else:
        return ResponseJson({"status": 0, "msg": "您未登录"})
