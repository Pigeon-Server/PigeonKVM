import json
from time import time, sleep, strftime, localtime
import cv2
import os
from copy import copy
from threading import Thread
import app.apis.WebSocket.control
import app.util.Config as Config

import numpy as np

from app.util.logger import Log


class camera:
    # 采集卡
    __camera = None
    # 未处理的采集卡帧
    __cameraFrame = None
    # 前一张采集卡帧
    __before = None
    # 后一张采集卡帧
    __after = None
    __flag = 0
    __op = None
    # 录制参数
    __recordArgs = {
        "User": None,
        "Machine": None,
        "DevMode": False
    }
    # 状态
    __status = {
        "GetFrame": True,
        "GetFrameThread": True,
        "RecordVideo": 0
    }

    def __init__(self, camera_id=0):
        Log.info("采集卡初始化中....")

        for i in range(0, 10):
            self.__camera = cv2.VideoCapture(camera_id)

            # 视频宽度
            self.__camera.set(cv2.CAP_PROP_FRAME_WIDTH, Config.main_config.get("camera").get("width"))
            # 视频高度
            self.__camera.set(cv2.CAP_PROP_FRAME_HEIGHT, Config.main_config.get("camera").get("height"))
            # 视频格式
            self.__camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
            # 视频帧率
            self.__camera.set(cv2.CAP_PROP_FPS, Config.main_config.get("camera").get("fps"))
            # 视频亮度
            self.__camera.set(10, Config.main_config.get("camera").get("brightness"))
            # 视频曝光
            self.__camera.set(cv2.CAP_PROP_EXPOSURE, Config.main_config.get("camera").get("exposure"))
            # 饱和度
            self.__camera.set(12, Config.main_config.get("camera").get("colorfulness"))
            # 色调
            self.__camera.set(13, Config.main_config.get("camera").get("tonal"))

            if self.__camera.isOpened():
                Log.info("采集卡启动成功")
                break
            sleep(2)
        Log.success("采集卡初始化完成")
        # 获取采集卡帧线程
        Thread(target=self.__GetFrame, args=(), name="getFrame").start()

    def __del__(self):
        """销毁时"""
        # 停止获取采集卡帧
        self.__status["GetFrame"] = False
        # 停止录制
        self.__status["RecordVideo"] = 0
        # 停止采集卡线程
        self.__status["GetFrameThread"] = False
        # 销毁摄像头
        self.__camera.release()
        if not self.__camera.isOpened():
            Log.success("采集卡实例已销毁")

    def isOpened(self):
        """查询摄像头是否开启"""
        return self.__camera.isOpened()
    
    @Log.catch
    def __movingDetect(self, frame1, frame2):
        """检测图片是否变动"""
        img1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        img2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        grey_diff = cv2.absdiff(img1, img2)  # 计算两幅图的像素差
        change = np.average(grey_diff)
        # 当两幅图的差异大于给定的值后，认为画面有物体在动
        if change > Config.main_config.get("camera").get("updateDisplayChange"):
            if app.apis.WebSocket.control.links.get(self.__op):
                try:
                    app.apis.WebSocket.control.controlPageWebSocket.send(
                        app.apis.WebSocket.control.links.get(self.__op),
                        bytes_data=self.getDisplayFrame()
                    )
                except Exception as e:
                    Log.error(f"发送帧错误\n{e}")
        return

    @Log.catch
    def __GetFrame(self):
        """获取采集卡画面

        Raises:
            RuntimeError: _description_
        """
        while self.__status["GetFrameThread"]:
            if self.__status["GetFrame"]:
                ret, self.__cameraFrame = self.__camera.read()
                if not ret:
                    self.__status["GetFrame"] = False
                    Log.error("帧拉取失败")
                    break
                else:
                    if self.__flag == 0:
                        self.__after = copy(self.__cameraFrame)
                        self.__flag = 1
                    elif self.__flag == 1:
                        self.__before = copy(self.__cameraFrame)
                        self.__flag = 0

                    if (self.__after is not None and self.__before is not None) and (Config.main_config.get("main").get("record") is False or self.__op is not None):
                        Thread(target=self.__movingDetect, args=(self.__after, self.__before,), name="movingDetect").start()
            else:
                sleep(0.5)
        return
    
    def setOp(self,value):
        self.__op = value
        Log.debug(f"已设置操作员:{value}")

    def stopGetFrame(self):
        self.__status["GetFrameThread"] = False
        Log.success("获取帧已停止")

    @Log.catch
    def __processFrame(self):
        """处理要保存的视频帧"""
        frame = copy(self.__cameraFrame)
        cv2.putText(
            frame,  # 图像
            f"Orange Pi IPKVM {strftime('%Y-%m-%d %H:%M:%S', localtime())}",  # 水印文字
            (10, 20),  # 坐标
            cv2.FONT_HERSHEY_SIMPLEX,  # 字体
            0.5,  # 字体大小
            (255, 255, 255),  # 颜色
            1,  # 线宽
            cv2.LINE_AA,  # 线型
            False  # 起始位置
        )
        cv2.putText(
            frame,  # 图像
            f"Operating User: {self.__recordArgs.get('User')}",  # 水印文字
            (10, 40),  # 坐标
            cv2.FONT_HERSHEY_SIMPLEX,  # 字体
            0.5,  # 字体大小
            (255, 255, 255),  # 颜色
            1,  # 线宽
            cv2.LINE_AA,  # 线型
            False  # 起始位置
        )
        cv2.putText(
            frame,  # 图像
            f"Machine: {self.__recordArgs.get('Machine')}",  # 水印文字
            (10, 60),  # 坐标
            cv2.FONT_HERSHEY_SIMPLEX,  # 字体
            0.5,  # 字体大小
            (255, 255, 255),  # 颜色
            1,  # 线宽
            cv2.LINE_AA,  # 线型
            False  # 起始位置
        )
        if self.__recordArgs.get("DevMode"):
            cv2.putText(
                frame,  # 图像
                f"Dev Mode!!!",  # 水印文字
                (10, 85),  # 坐标
                cv2.FONT_HERSHEY_SIMPLEX,  # 字体
                0.8,  # 字体大小
                (0, 255, 0),  # 颜色
                1,  # 线宽
                cv2.LINE_AA,  # 线型
                False  # 起始位置
            )
        return frame

    @Log.catch
    def __recordVideo(self):
        """启动视频录制"""
        machine = self.__recordArgs.get("Machine")
        startTime = strftime('%Y-%m-%d %H-%M-%S', localtime())
        if not os.path.exists("record"):
            os.mkdir("record")
            Log.info("由于record文件夹不存在，已自动创建")
        outputFileName = os.path.join('record', f'output_{startTime}-not_finished.avi')
        videoOut = cv2.VideoWriter(
            outputFileName,  # 输出文件名
            cv2.VideoWriter_fourcc(*'DIVX'),  # 编码器
            Config.main_config.get("record").get("fps"),  # 输出帧率
            (int(self.__camera.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self.__camera.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        )  # 写入视频
        Log.success("采集卡录制已启动，开始时间：" + startTime)
        while self.__status.get("RecordVideo") != 0:
            match self.__status.get("RecordVideo"):
                case 1:
                    videoOut.write(self.__processFrame())  # 写入帧
                case 2:
                    sleep(0.5)
        else:
            videoOut.release()
            os.rename(outputFileName,
                      os.path.join('record', f'[{machine}]output_{startTime}——{strftime("%Y-%m-%d %H-%M-%S", localtime())}.avi'))
            Log.info(f"录制已停止：{startTime}——{strftime('%H-%M-%S', localtime())}")
        Log.success("采集卡录制已停止")
        return

    def startRecord(self, op_user=None, machine_name=None, fps=24, dev=False):
        """启动后台录制

        Args:
            op_user (str): 操作员，在录制水印中显示. Defaults to None.
            machine_name (str): 操作的机器，在录制水印中显示. Defaults to None.
            dev (bool): 开发模式，会在录制水印中显示
            fps (int): 录制的fps
        """
        if self.__status["RecordVideo"] == 0:
            self.__recordArgs["User"] = op_user
            self.__recordArgs["Machine"] = machine_name
            self.__recordArgs["DevMode"] = dev
            self.__status["RecordVideo"] = 1
            Log.info("采集卡录制正在启动")
            Thread(target=self.__recordVideo, args=(), name="RecordVideo").start()
        else:
            Log.warning("录制已经在进行了")

    def pauseRecord(self):
        """暂停后台录制（应在用户无操作达到一定时间时触发）"""
        Log.info("采集卡录制已暂停")
        self.__status["RecordVideo"] = 2

    def stopRecord(self):
        """停止后台录制"""
        if self.__status["RecordVideo"] != 0:
            Log.info("采集卡录制正在停止")
            self.__status["RecordVideo"] = 0
            self.__recordArgs["User"] = None
            self.__recordArgs["Machine"] = None
            self.__recordArgs["DevMode"] = False
        else:
            Log.warning("录制未开始")

    def getRecordStatus(self):
        return self.__status["RecordVideo"]

    def getDisplayFrame(self):
        """获取用于web显示的采集卡帧"""
        return cv2.imencode(".jpg", self.__cameraFrame)[1].tobytes()
