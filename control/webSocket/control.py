import json

from channels.exceptions import StopConsumer
from channels.generic.websocket import WebsocketConsumer
from django.apps import apps

import app.apps as app
from util.logger import Log
from control.util.HID_control import HID_control
# import control.util.camera as camera
from setting.entity.Config import config

links = {}

class control(WebsocketConsumer):
    __userID: int = None
    __clientIP: str = None
    __controller = None
    __camera = None
    __config: config = None
    __baseConfig = None

    def connect(self):
        # 在建立连接时执行的操作
        user = self.scope["session"].get("user")
        self.__userID = self.scope["session"].get("userID")
        self.__clientIP = self.scope["client"][0]
        self.__controller = HID_control(1920, 1080)
        self.__camera = apps.get_app_config('control').get_camera()
        self.__config = apps.get_app_config('setting').get_config()
        self.__baseConfig = apps.get_app_config('setting').get_base_config()

        if user:
            from app.util.DataBaseTools import writeAccessLog, writeAudit
            self.accept()
            links.update({user: self})
            writeAccessLog(self.__userID, self.__clientIP, "Control Page Websocket Connect")
            writeAudit(self.__userID, "Control Start", "control", "")
            if apps.get_app_config("setting").get_base_config().get("main").get("record"):
                self.__camera.startRecord(op_user=user, machine_name="DEV")
                writeAudit(self.__userID, "Recording starts", "control", "")
            self.__camera.setOp(user)
            self.sendJson({
                "method": "init",
                "data": {
                    "display": {
                        "width": self.__config.camera.width,
                        "height": self.__config.camera.height,
                    }
                }
            })
            self.send(bytes_data=self.__camera.getDisplayFrame())
        else:
            self.close(-1)

    def disconnect(self, close_code):
        from app.util.DataBaseTools import writeAccessLog, writeAudit
        # 在断开连接时执行的操作
        user = self.scope["session"].get("user")
        if self.__baseConfig.get("main").get("record"):
            self.__camera.stopRecord()
            writeAudit(self.__userID, "Recording ends", "control", "")
        self.__camera.setOp(None)
        links.pop(user)
        writeAccessLog(self.__userID, self.__clientIP, f"Control Page Websocket Disconnect(Code:{close_code})")
        writeAudit(self.__userID, "Control ends", "control", "")
        raise StopConsumer

    def receive(self, text_data: str, bytes_data: bytes = None):
        # 处理接收到的消息
        try:
            jsonData = json.loads(text_data)
        except Exception as e:
            Log.error(f"解析Websocket消息时发生错误：\n{e}")
        else:
            if jsonData.get("method"):
                pass
                # match jsonData.get("method"):
                #     # 鼠标按键 - 抬起
                #     case "mouseup":
                #         self.__controller.mouseup()
                #     # 鼠标按键 - 按下
                #     case "mousedown":
                #         self.__controller.mousedown()
                #     # 鼠标 - 移动
                #     case "mousemove":
                #         self.__controller.mousemove()
                #     case "mouseScroll":
                #         self.__controller.mouseScroll()
                #     # 键盘 - 按下
                #     case "keydown":
                #         self.__controller.keydown()
                #     # 键盘 - 抬起
                #     case "keyup":
                #         self.__controller.keyup()
                #     # 粘贴
                #     case "paste":
                #         text = jsonData.get("data").get("String")
                #         self.__controller.paste_text(text)
                #     case _:
                #         Log.error("未能解析的操作方法")

    def sendJson(self, data):
        self.send(json.dumps(data))
