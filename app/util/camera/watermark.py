from time import strftime, localtime

import cv2

from util.logger import Log
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os

@Log.catch
def createWatermarkImage(width: int, height: int, text: str, font_path=os.path.join(os.getcwd(),"font/Noto_Sans_SC/NotoSansSC-Medium.otf",), font_size=16, density=0.2)->np.array:
    """
    创建水印图片
    :param width: 水印图片宽度
    :param height:  水印图片高度
    :param text: 水印文字
    :param font_path: 字体路径
    :param font_size: 字体大小
    :param density: 密度
    :return: np.array
    """
    # 创建一个透明的水印图片
    watermark = np.zeros((height, width, 4), dtype=np.uint8)
    # 使用默认字体或加载自定义字体
    if font_path is not None and os.path.exists(font_path):
        custom_font = ImageFont.truetype(font_path, size=font_size)
    else:
        custom_font = ImageFont.load_default()
    # 使用PIL库添加文字水印
    pil_watermark = Image.fromarray(watermark)
    draw = ImageDraw.Draw(pil_watermark, 'RGBA')
    # 计算水印的密度
    num_watermarks = int(width * density)
    # 计算水印的间隔，确保水印图像不超过原始图像的范围
    interval = int(width / num_watermarks)
    # 在整张画面添加水印
    for y in range(0, height, font_size + 35 + interval):
        for x in range(0, width, font_size + 150 + interval):
            draw.text((x, y), text, font=custom_font, fill=(255, 255, 255, 255))
    # 转换为NumPy数组
    return np.array(pil_watermark)

@Log.catch
def loadWatermarkToImage(frame, watermark: np.array, alpha=0.05):
    """
    加载水印到图像中
    :param frame: 图像帧
    :param watermark: 水印数组
    :param alpha: 透明度
    :return: frame
    """
    # # 将水印叠加到原始图片上
    if watermark is not None:
        return cv2.addWeighted(cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA), 1 - alpha, watermark, alpha, 0)
    return frame

@Log.catch
def processSaveFrame(frame, user: str, machine: str, dev_mode: bool = False):
    """
    处理保存视频帧
    :param frame: 帧
    :param user: 用户
    :param machine: 机器名
    :param dev_mode: 是否为开发模式
    :return: frame
    """
    cv2.putText(
        frame,  # 图像
        f"PigeonKVM {strftime('%Y-%m-%d %H:%M:%S', localtime())}",  # 水印文字
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
        f"Operating User: {user}",  # 水印文字
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
        f"Machine: {machine}",  # 水印文字
        (10, 60),  # 坐标
        cv2.FONT_HERSHEY_SIMPLEX,  # 字体
        0.5,  # 字体大小
        (255, 255, 255),  # 颜色
        1,  # 线宽
        cv2.LINE_AA,  # 线型
        False  # 起始位置
    )
    if dev_mode:
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