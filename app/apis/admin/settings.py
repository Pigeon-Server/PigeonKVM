import json

import app.util.Config as config
from django.shortcuts import HttpResponse

from app.util.Request import RequestLoadJson
from app.util.Response import ResponseJson
from app.util.logger import Log


def getSetting(req):
    return HttpResponse(json.dumps(config.config, default=lambda o: o.__dict__, indent=2))

def editSetting(req):
    if req.method == 'POST':
        try:
            req_json = RequestLoadJson(req)
        except Exception as e:
            Log.error(e)
            return ResponseJson({"status": -1, "msg": "JSON解析失败"})
        else:
            config.config = config.saveConfig(config.saveConfig(config.dictToConfig(req_json, config.configObj)))
            return HttpResponse(json.dumps(config.config, default=lambda o: o.__dict__, indent=2))

    else:
        return ResponseJson({"status": -1, "msg": "请求方式不正确"})