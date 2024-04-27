from util.logger import Log
from app.util.DataBaseTools import writeAudit
import app.apps as apps
from util.Request import RequestLoadJson
from util.Response import ResponseJson


def fastInput(req):
    if req.method == "POST":
        try:
            req_json = RequestLoadJson(req)
        except Exception as e:
            Log.error(e)
            return ResponseJson({"status": -1, "msg": f"JSON解析失败:{e}"})
        else:
            inputString = req_json.get("input")
            userId = req.session.get("userID")
            try:
                apps.HID.inputString(str(inputString))
                writeAudit(userId, "fastInputString", "control", inputString)
                return ResponseJson({
                    "status": 1,
                    "msg": "成功"
                })
            except Exception as err:
                Log.error(err)
                return ResponseJson({
                    "status": 0,
                    "msg": "失败"
                })
    else:
        return ResponseJson({"status": -1, "msg": "请求方式不正确"})

def clickButton(req):
    if req.method == "POST":
        try:
            req_json = RequestLoadJson(req)
        except Exception as e:
            Log.error(e)
            return ResponseJson({"status": -1, "msg": f"JSON解析失败:{e}"})
        else:
            button = req_json.get("button")
            userId = req.session.get("userID")
            return ResponseJson({
                "status": 0,
                "msg": "未实现"
            })

    else:
        return ResponseJson({"status": -1, "msg": "请求方式不正确"})


def connectDevice(req):
    if req.method == "POST":
        try:
            req_json = RequestLoadJson(req)
        except Exception as e:
            Log.error(e)
            return ResponseJson({"status": -1, "msg": f"JSON解析失败:{e}"})
        else:
            deviceName = req_json.get("button")
            userId = req.session.get("userID")
            return ResponseJson({
                "status": 0,
                "msg": "未实现"
            })

    else:
        return ResponseJson({"status": -1, "msg": "请求方式不正确"})

def getLedStatus(req):
    return ResponseJson({
        "status": 0,
        "msg": "未实现"
    })