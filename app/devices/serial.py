# import serial.Serial as Serial
import re
import os
import serial as pyserial
from time import sleep

from serial import Serial
from threading import Thread
from queue import Queue
from app.util.logger import Log


class serialConfig:
    post: str
    baudrate: int
    auto_reconnect: bool
    auto_reconnect_time: int

    def __init__(self, post: str, baudrate: int, auto_reconnect: bool, auto_reconnect_time: int):
        self.post = post
        self.baudrate = baudrate
        self.auto_reconnect = auto_reconnect
        self.auto_reconnect_time = auto_reconnect_time

class serial:
    __serial: Serial = None
    __config: serialConfig = None
    __flag: bool = True
    __count: int = 0
    __writeQueue: Queue = None

    def __init__(self, post: str, baudrate: int = 9600, auto_reconnect: bool = False, auto_reconnect_time: int = 1):
        """
        :param post: 端口
        :param baudrate: 波特率
        :param auto_reconnect: 自动重连
        :param auto_reconnect_time: 重连间隔时间(秒)
        """
        self.__config = serialConfig(post, baudrate, auto_reconnect, auto_reconnect_time)
        if re.match(r"^/dev/.+", post) and not os.path.exists(post):
            raise FileNotFoundError(f"{post} not exist")
        self.__OpenSerial()
        self.__writeQueue = Queue()
        if self.__config.auto_reconnect:
            Thread(target=self.__autoReconnect, name="serialAutoReconnectThread").start()
            Thread(target=self.__writeQueueThread(), name="serialWriteQueueThread").start()

    def __OpenSerial(self):
        """
        打开串口
        :return:
        """
        try:
            self.__serial = Serial(self.__config.post, self.__config.baudrate)
        except FileNotFoundError:
            self.__serial = None
        else:
            if self.isOpen():
                self.__count = 0

    def __autoReconnect(self):
        """自动重新连接守护进程"""
        while self.__count < 3:
            sleep(0.1)
            if self.__serial is None:
                break
            if not self.isOpen():
                self.__count += 1
                sleep(self.__config.auto_reconnect_time)
                self.__OpenSerial()
        raise RuntimeError("Serial lost connection")

    def __writeQueueThread(self):
        """串口写入线程"""
        while self.__flag:
            if self.__writeQueue.not_empty and self.isOpen():
                self.__serial.write(self.__writeQueue.get())
            else:
                sleep(0.1)

    def getSerialConfig(self) -> serialConfig:
        """
        获取串口连接配置
        :return(serialConfig):
        """
        return self.__config

    def isOpen(self) -> bool:
        """
        串口是否打开
        :return(bool):
        """
        if self.__serial is not None:
            return self.__serial.isOpen()
        else:
            return False

    def read(self, size: int = 1):
        if self.isOpen():
            return self.__serial.read(size)
        else:
            return None


    def read_until(self, expected: pyserial.serialutil = pyserial.serialutil.LF, size=None):
        if self.isOpen():
            return self.__serial.read_until(expected, size)
        else:
            return None

    def write(self, data):
        """
        在串口队列添加写入事务
        :param data: 要写入的数据
        :return: None
        """
        if self.isOpen():
            self.__writeQueue.put(data)
        else:
            raise RuntimeError("Serial is not open")

    def flush(self) -> bool:
        """文件类对象的刷新，需等待所有数据被写入"""
        if self.isOpen():
            self.__serial.flush()
            return True
        else:
            raise RuntimeError("Serial is not open")

    def inWaiting(self) -> int:
        """获取输入缓冲区中的字节数"""
        if self.isOpen():
            return self.__serial.inWaiting()
        else:
            raise RuntimeError("Serial is not open")

    def outWaiting(self) -> int:
        """获取输出缓冲区中的字节数 仅Windows"""
        if self.isOpen():
            return self.__serial.outWaiting()
        else:
            raise RuntimeError("Serial is not open")

    def flushInput(self) -> bool:
        """清空输入缓冲区，不清空队列"""
        if self.isOpen():
            self.__serial.flushInput()
            return True
        else:
            raise RuntimeError("Serial is not open")

    def flushOutput(self):
        """清空输出缓冲区，中止当前输出并丢弃缓冲区中的所有内容"""
        if self.isOpen():
            self.__serial.flushOutput()
            return True
        else:
            raise RuntimeError("Serial is not open")

    def send_break(self, duration: float = 0.25):
        """发送中断"""
        if self.isOpen():
            self.__serial.send_break(duration)
            return True
        else:
            raise RuntimeError("Serial is not open")

    def get_break_condition(self) -> bool:
        """获取当前中断状态"""
        if self.isOpen():
            return self.__serial.break_condition
        else:
            raise RuntimeError("Serial is not open")

    def set_break_condition(self, value: bool):
        """设置中断状态"""
        if self.isOpen():
            self.__serial.break_condition = value
            return True
        else:
            raise RuntimeError("Serial is not open")

    def get_rts(self) -> bool:
        """获取RTS线路的状态"""
        if self.isOpen():
            return self.__serial.rts
        else:
            raise RuntimeError("Serial is not open")

    def set_rts(self, value: bool):
        """设置RTS线路的状态"""
        if self.isOpen():
            self.__serial.rts = value
        else:
            raise RuntimeError("Serial is not open")

    def get_dtr(self) -> bool:
        """获取DTR线的状态"""
        if self.isOpen():
            return self.__serial.dtr
        else:
            raise RuntimeError("Serial is not open")

    def set_dtr(self, value: bool):
        """设置DTR线的状态"""
        if self.isOpen():
            self.__serial.dtr = value
        else:
            raise RuntimeError("Serial is not open")

    def name(self) -> str:
        """获取设备名称"""
        if self.isOpen():
            return self.__serial.name
        else:
            raise RuntimeError("Serial is not open")

    def close(self):
        """
        关闭串口
        :return:
        """
        if self.isOpen():
            self.__serial.close()
            self.__flag = False
        else:
            raise RuntimeError("Serial is not open")

    def getSerialObject(self) -> Serial:
        """
        获取串口对象
        :return:
        """
        return self.__serial