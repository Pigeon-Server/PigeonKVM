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
        password = req_json.get("password")
        password = PasswordToMd5(password)
        if Users.objects.filter(userName=user, password=password):
            User = Users.objects.filter(userName=user, password=password).first()
            if not User.disable:
                req.session["user"] = user
                req.session["userID"] = User.id
                req.session.set_expiry(int(Config.main_config.get("main").get("sessionExpiry")) * 60)
                Log.success(f"用户[{user}]已登陆")
                User.lastLoginIP = getClientIp(req)
                User.lastLoginTime = datetime.datetime.now()
                User.save()
                writeAudit(User.id, "Login", "Auth", User.lastLoginIP)
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
        user = req.session.get("user")
        userId = req.session.get("UserID")
        req.session.clear()
        Log.success(f"用户[{user}]已登出")
        writeAudit(userId, "Outlog", "Auth", getClientIp(req))
        return ResponseJson({"status": 1, "msg": "登出成功"})
    else:
        return ResponseJson({"status": 0, "msg": "您未登录"})
