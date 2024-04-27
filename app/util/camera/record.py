import os
from time import strftime, localtime, sleep

import cv2

from util.logger import Log


class record:
    __VideoWriter = None
    __config = None
    __startTime = None

    class __record_config:
        """录制设置"""
        camera = None
        width = None
        height = None
        fps = None
        username = None
        machine_name = None
        dev_mode = None

        def __init__(self, camera, width: int, height: int, fps: int, username: str, machine_name: str, dev_mode: bool):
            """
            初始化设置
            :param camera: 相机
            :param width: 宽
            :param height: 高
            :param fps: 帧率
            :param username: 用户名
            :param machine_name: 机器名
            :param dev_mode: 是否为开发模式
            """
            self.camera = camera
            self.width = width
            self.height = height
            self.fps = fps
            self.username = username
            self.machine_name = machine_name
            self.dev_mode = dev_mode

        def clean(self):
            """
            清除设置项
            :return:
            """
            self.camera = None
            self.width = None
            self.height = None
            self.fps = None
            self.username = None
            self.machine_name = None
            self.dev_mode = None

    def start(self, cv2_camera, width: int, height: int, fps: int, username: str, machine_name: str, dev_mode: bool):
        if not os.path.exists("record"):
            os.mkdir("record")
            Log.info("由于record文件夹不存在，已自动创建")
        self.__config = self.__record_config(cv2_camera, width, height, fps, username, machine_name, dev_mode)
        self.__startTime = strftime('%Y-%m-%d %H-%M-%S', localtime())
        outputFileName = os.path.join('record', f'output_{self.__startTime}-not_finished.avi')

    def stop(self):
        pass

    def pause(self):
        pass

    def init_record(self, ):


        videoOut = cv2.VideoWriter(
            outputFileName,  # 输出文件名
            cv2.VideoWriter_fourcc(*'DIVX'),  # 编码器
            fps,  # 输出帧率
            (width, height)
        )



@Log.catch
def recordVideo(frame, ):
    """
    录制视频
    :param frame:
    :param width:
    :param height:
    :param fps:
    :param machine:
    :return:
    """

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
                  os.path.join('record',
                               f'[{machine}]output_{startTime}——{strftime("%Y-%m-%d %H-%M-%S", localtime())}.avi'))
        Log.info(f"录制已停止：{startTime}——{strftime('%H-%M-%S', localtime())}")
    Log.success("采集卡录制已停止")
    return
