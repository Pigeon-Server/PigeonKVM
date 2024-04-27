from django.urls import path
from control.webSocket.control import control
from app.apis.WebSocket.fileManager import fileManagerPageWebSocket
# from app.apis.WebSocket.userManager import userManagerWebSocket
from app.apis.WebSocket.statusBar import statusBarModuleWebSocket

websocket_urlpatterns = [
    # 控制页
    path(r"api/websocket/control", control.as_asgi()),
    # 文件管理页
    path(r"api/websocket/fileManager", fileManagerPageWebSocket.as_asgi()),
    # 用户管理页
    # path(r"api/websocket/userManager", userManagerWebSocket.as_asgi()),
    # 状态栏模块
    path(r"api/websocket/statusBar", statusBarModuleWebSocket.as_asgi())
]