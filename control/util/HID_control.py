from django.apps import apps
from control.util.ch9329 import ch3929


class HID_control:
    __width: int = None
    __height: int = None
    __HID_DEVICE: ch3929 = None

    def __init__(self, width, height):
        """
        :param width: 屏幕宽度（px）
        :param height: 屏幕高度（px）
        """
        self.__width = width
        self.__height = height
        self.__HID_DEVICE = apps.get_app_config("control").get_device()

    def mouseup(self, x, y):
        """
        鼠标抬起
        :param x: x坐标
        :param y: y坐标
        :return: None
        """
        self.__HID_DEVICE.Mouse(
            x_move=x,
            y_move=y,
            x_max=self.__width,
            y_max=self.__height
        )

    def mousedown(self, x, y, button):
        """
        鼠标按下
        :param x: x坐标
        :param y: y坐标
        :param button: 按键
        :return: None
        """
        self.__HID_DEVICE.Mouse(
            x_move=x,
            y_move=y,
            button=button,
            x_max=self.__width,
            y_max=self.__height
        )

    def mousemove(self, x, y, button):
        """
        鼠标移动
        :param x: x坐标
        :param y: y坐标
        :param button: 按键
        :return: None
        """
        self.__HID_DEVICE.Mouse(
            x_move=x,
            y_move=y,
            button=button,
            x_max=self.__width,
            y_max=self.__height
        )

    def mouseScroll(self, x, y, direction, distance: int = 1):
        """
        鼠标滚动
        :param x: x坐标
        :param y: y坐标
        :param direction: 滚动方向
        :param distance: 滚动距离
        :return: None
        """
        self.__HID_DEVICE.Mouse(
            x_move=x,
            y_move=y,
            distance=distance,
            direction=direction,
            x_max=self.__width,
            y_max=self.__height
        )

    def keydown(self, key, code):
        """
        键盘按下
        :param key: 键
        :param code: 键码
        :return: None
        """
        if key in ["Enter", "Shift", "Ctrl", "Alt"]:
            self.__HID_DEVICE.keyBoardInput(code)
        else:
            self.__HID_DEVICE.keyBoardInput(key)
        # app.HID.keyBoardInput(key)

    def keyup(self):
        """
        全部键抬起
        :return: None
        """
        self.__HID_DEVICE.keyBoardInput(mode="Clear")

    def paste_text(self, text: str):
        """
        粘贴文本（仅支持英文及半角字符）
        :param text: 文本
        :return: None
        """
        self.__HID_DEVICE.inputString(text)
