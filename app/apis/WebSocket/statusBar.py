import json

from channels.exceptions import StopConsumer
from channels.generic.websocket import WebsocketConsumer

import app.apps as app
import app.util.Config as Config
from app.util.logger import Log

links = {}

class statusBarModuleWebSocket(WebsocketConsumer):

    def connect(self):
        # 在建立连接时执行的操作
        user = self.scope["session"].get("user")
        if user:
            self.accept()
            links.update({user: self})
            Log.success(f"用户{user}已连接")
        else:
            self.close(-1)

    def disconnect(self, close_code):
        # 在断开连接时执行的操作
        user = self.scope["session"].get("user")
        links.pop(user)
        Log.success(f"用户{user}已断开({close_code})")
        raise StopConsumer

    def receive(self, text_data=None, bytes_data=None):
        # 处理接收到的消息
        Log.debug(text_data)

        if text_data:
            try:
                jsonData = json.loads(text_data)
            except Exception as e:
                print(f"解析Websocket消息时发生错误：\n{e}")
            else:
                pass

    def sendJson(self, data):
        self.send(json.dumps(data))
