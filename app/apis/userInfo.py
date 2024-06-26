# 修改用户信息
import base64
import hashlib
import os

from django.http import FileResponse
from app.models import Users
from app.util.PasswordTools import PasswordToMd5, verifyPasswordRules
from util.Request import RequestLoadJson, getClientIp
from util.Response import ResponseJson
from util.logger import Log
from app.util.DataBaseTools import writeAudit, writeAccessLog, writeFileChangeLog
from app.util.permission import groupPermission


@Log.catch
def setPassword(req):
    """
    设置密码
    :param req:
    :return:
    """
    if req.method == 'POST':
        try:
            req_json = RequestLoadJson(req)
        except Exception as e:
            Log.error(e)
            return ResponseJson({"status": -1, "msg": "JSON解析失败"})
        else:
            userId = req.session.get("userID")
            data = req_json.get("data")
            oldPassword = PasswordToMd5(data.get("oldPassword"))
            newPassword = data.get("newPassword")
            if not (userId or data or oldPassword or newPassword):
                return ResponseJson({"status": -1, "msg": "参数不完整"})
            User = Users.objects.filter(id=userId).first()
            Log.debug(User.id)
            if not verifyPasswordRules(newPassword):
                return ResponseJson({"status": 0, "msg": "新密码格式不合规（至少6字符，必须含有数字，小写字母，大写字母，特殊字符）"})
            if oldPassword != User.password:
                return ResponseJson({"status": 0, "msg": "原密码不正确"})

            User.password = PasswordToMd5(newPassword)
            User.save()
            writeAudit(userId, "Set Password(设置密码)",
                       "User Info(用户信息)",
                       "None")
            return ResponseJson({"status": 1, "msg": "密码修改成功"})
    else:
        return ResponseJson({"status": -1, "msg": "请求方式不正确"})


def getUserInfo(req):
    """
    获取用户信息
    :param req:
    :return:
    """
    userId = req.session.get("userID")
    if userId:
        User = Users.objects.filter(id=userId).first()
        User_Permission = groupPermission(User.permission_id) if User.permission_id else None

        writeAccessLog(userId, getClientIp(req), "Get User Info")
        return ResponseJson({"status": 1, "data": {
            "id": User.id,
            "userName": User.userName,
            "realName": User.realName,
            "email": User.email,
            "group": User_Permission.get_group_name() if User_Permission else None,
            "permissions": User_Permission.get_permissions_dict() if User_Permission else None,
        }})
    else:
        return ResponseJson({"status": -1, "msg": "未登录"})

def setUserInfo(req):
    """
    设置用户信息
    :param req:
    :return:
    """
    if req.method == 'POST':
        try:
            req_json = RequestLoadJson(req)
        except Exception as e:
            Log.error(e)
            return ResponseJson({"status": -1, "msg": "JSON解析失败"})
        else:
            userId = req.session.get("userID")
            data = req_json.get("data")
            if userId and data:
                User = Users.objects.filter(id=userId).first()
                userName = data.get("userName")
                realName = data.get("realName")
                email = data.get("email")
                if userName and userName != User.userName:
                    if Users.objects.filter(userName=userName):
                        return ResponseJson({"status": 0, "msg": "用户名已存在"})
                    writeAudit(userId, "Set User Info(设置用户信息): Update User Name(更新用户名)",
                               "User Info(用户信息)",
                               f"{User.userName}-->{userName}")
                    User.userName = userName
                    req.session["user"] = userName
                # if realName and realName != User.realName:
                #     if Users.objects.filter(realName=realName):
                #         return ResponseJson({"status": 0, "msg": "该姓名用户已存在"})
                #     writeAudit(userId, "Set User Info(设置用户信息): Update Real Name(更新用户姓名)",
                #                "User Info(用户信息)",
                #                f"{User.realName}-->{realName}")
                #     User.realName = realName
                if email and email != User.email:
                    if Users.objects.filter(email=email):
                        return ResponseJson({"status": 0, "msg": "邮箱已被使用过啦"})
                    writeAudit(userId, "Set User Info(设置用户信息): Update Email(更新电子邮箱)",
                               "User Info(用户信息)",
                               f"{User.email}-->{email}")
                    User.email = email
                User.save()
                return ResponseJson({"status": 1, "msg": "成功", "data": {
                    "userName": User.userName,
                    "realName": User.realName,
                    "email": User.email,
                }})
            else:
                return ResponseJson({"status": -1, "msg": "参数不完整"})
    else:
        return ResponseJson({"status": -1, "msg": "请求方式不正确"})


# 头像上传
def uploadAvatar(req):
    """
    头像上传
    :param req:
    :return: JSON
    """
    if req.method == 'POST':
        try:
            req_json = RequestLoadJson(req)
        except Exception as e:
            Log.error(e)
            return ResponseJson({"status": -1, "msg": "JSON解析失败"})
        else:
            userId = req.session.get("userID")
            data = req_json.get("data")
            if not userId:
                return ResponseJson({"status": -1, "msg": "用户未登录"})
            if not data:
                return ResponseJson({"status": -1, "msg": "参数不完整（无数据）"})
            avatarImgBase64 = data.get("avatarImg")
            avatarImgHash = data.get("avatarHash")
            if avatarImgBase64 and avatarImgHash:
                if not os.path.exists("avatar"):
                    os.mkdir("avatar")

                if os.path.exists(os.path.join("avatar", f"{avatarImgHash}")):
                    Log.debug("文件已存在，跳过写入")
                    User = Users.objects.filter(id=req.session.get("userID")).first()
                    if avatarImgHash != User.avatar:
                        User.avatar = avatarImgHash
                        User.save()
                    return ResponseJson({"status": 1, "msg": "上传成功"})

                dataBytes = base64.b64decode(avatarImgBase64.split(",")[1])

                with open(os.path.join("avatar", f"{avatarImgHash}"), "wb+") as f:
                    md5 = hashlib.md5()
                    md5.update(dataBytes)

                    saveFileMd5 = md5.hexdigest()

                    if saveFileMd5 == avatarImgHash:
                        Log.debug("头像上传Md5验证成功")
                        f.write(dataBytes)
                        User = Users.objects.filter(id=userId).first()
                        User.avatar = avatarImgHash
                        User.save()
                        writeAudit(userId, "Upload Avatar(上传头像)",
                                   "User Info(用户信息)",
                                   saveFileMd5)
                        writeFileChangeLog(userId, "Upload File", os.path.join("avatar", f"{avatarImgHash}"))
                        return ResponseJson({"status": 1, "msg": "上传成功"})
                    else:
                        Log.warning(f"Md5验证失败(发送时：{avatarImgHash} 接收时：{saveFileMd5})")
                        try:
                            os.remove(os.path.join("avatar", f"{avatarImgHash}"))
                        except Exception as err:
                            Log.error(err)
                        return ResponseJson({"status": 0, "msg": f"Md5验证失败(发送时：{avatarImgHash} 接收时：{saveFileMd5})"})
            else:
                return ResponseJson({"status": -1, "msg": "参数不完整"})
    else:
        return ResponseJson({"status": -1, "msg": "请求方式不正确"})

def getAvatar(req):
    """
    获取用户头像
    :param req:
    :return: Image
    """
    userId = req.session.get("userID")

    if (not userId):
        return ResponseJson({"status": -1, "msg": "用户未登录"})

    User = Users.objects.filter(id=userId).first()
    writeAccessLog(userId, getClientIp(req), "Get Avatar")

    if not User.avatar:
        return FileResponse(open(os.path.join("avatar", "fff.png"), "rb"), content_type="image/png")
    if os.path.exists(os.path.join("avatar", User.avatar)):
        return FileResponse(open(os.path.join("avatar", User.avatar), "rb"), content_type="image/webp")