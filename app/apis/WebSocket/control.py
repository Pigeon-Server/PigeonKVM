import json

from channels.exceptions import StopConsumer
from channels.generic.websocket import WebsocketConsumer

import app.apps as app
import app.util.Config as Config
from app.util.logger import Log
from app.util.DataBaseTools import writeAccessLog, writeAudit

links = {}

class controlPageWebSocket(WebsocketConsumer):
    __userID = None
    __clientIP = None

    def connect(self):
        # 在建立连接时执行的操作
        user = self.scope["session"].get("user")
        self.__userID = self.scope["session"].get("userID")
        self.__clientIP = self.scope["client"][0]
        if user:
            self.accept()
            links.update({user: self})
            writeAccessLog(self.__userID, self.__clientIP, "Control Page Websocket Connect")
            writeAudit(self.__userID, "Control Start", "control", "")
            if Config.main_config.get("main").get("record"):
                app.cameraObj.startRecord(op_user=user, machine_name="DEV")
                writeAudit(self.__userID, "Recording starts", "control", "")
            app.cameraObj.setOp(user)
            self.sendJson({
                "method": "init",
                "data": {
                    "display": {
                        "width": Config.main_config.get("camera").get("width"),
                        "height": Config.main_config.get("camera").get("height"),
                    }
                }
            })
            self.send(bytes_data=app.cameraObj.getDisplayFrame())
        else:
            self.close(-1)

    def disconnect(self, close_code):
        # 在断开连接时执行的操作
        user = self.scope["session"].get("user")
        if Config.main_config.get("main").get("record"):
            app.cameraObj.stopRecord()
            writeAudit(self.__userID, "Recording ends", "control", "")
        app.cameraObj.setOp(None)
        links.pop(user)
        writeAccessLog(self.__userID, self.__clientIP, f"Control Page Websocket Disconnect(Code:{close_code})")
        writeAudit(self.__userID, "Control ends", "control", "")
        raise StopConsumer

    def receive(self, text_data):
        # 处理接收到的消息
        try:
            jsonData = json.loads(text_data)
        except Exception as e:
            Log.error(f"解析Websocket消息时发生错误：\n{e}")
        else:
            if jsonData.get("method"):
                match jsonData.get("method"):
                    # 鼠标按键 - 抬起
                    case "mouseup":
                        Log.debug("收到鼠标抬起请求")
                        x = jsonData.get("data").get("x")
                        y = jsonData.get("data").get("y")
                        app.HID.Mouse(
                            x_move=x,
                            y_move=y,
                            x_max=Config.main_config.get("camera").get("width"),
                            y_max=Config.main_config.get(
                                "camera").get("height")
                        )
                    # 鼠标按键 - 按下
                    case "mousedown":
                        Log.debug("收到鼠标按下请求")
                        x = jsonData.get("data").get("x")
                        y = jsonData.get("data").get("y")
                        button = jsonData.get("data").get("button")
                        app.HID.Mouse(
                            x_move=x,
                            y_move=y,
                            button=button,
                            x_max=Config.main_config.get("camera").get("width"),
                            y_max=Config.main_config.get(
                                "camera").get("height")
                        )
                    # 鼠标 - 移动
                    case "mousemove":
                        Log.debug("收到鼠标移动请求")
                        x = jsonData.get("data").get("x")
                        y = jsonData.get("data").get("y")
                        button = jsonData.get("data").get("button")
                        app.HID.Mouse(
                            x_move=x,
                            y_move=y,
                            button=button,
                            x_max=Config.main_config.get("camera").get("width"),
                            y_max=Config.main_config.get("camera").get("height")
                        )
                    case "mouseScroll":
                        Log.debug("收到鼠标滚动请求")
                        x = jsonData.get("data").get("x")
                        y = jsonData.get("data").get("y")
                        direction = jsonData.get("data").get("direction")
                        app.HID.Mouse(
                            x_move=x,
                            y_move=y,
                            distance=1, 
                            direction=direction,
                            x_max=Config.main_config.get("camera").get("width"),
                            y_max=Config.main_config.get(
                                "camera").get("height")
                        )
                    # 键盘 - 按下
                    case "keydown":
                        # TODO 待重构
                        Log.debug("收到键盘按下请求")
                        key = jsonData.get("data").get("key")
                        code = jsonData.get("data").get("code")
                        # if key in ["Enter", "Shift", "Ctrl", "Alt"]:
                        #     app.HID.keyBoardInput(code)
                        # else:
                        #     app.HID.keyBoardInput(key)
                        app.HID.keyBoardInput(key)
                    # 键盘 - 抬起
                    case "keyup":
                        Log.debug("收到键盘抬起请求")
                        app.HID.keyBoardInput(mode="Clear")
                    # 粘贴
                    case "paste":
                        inputString = jsonData.get("data").get("String")
                        app.HID.inputString(inputString)
                    case _:
                        Log.error("未能解析的操作方法")

    def sendJson(self, data):
        self.send(json.dumps(data))
