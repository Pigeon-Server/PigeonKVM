import binascii
import time
import serial
import manage
from queue import Queue 
from threading import Thread
from util.logger import Log


class ch3929:
    """命令码表"""
    __commandCode = {  # 芯片命令表
        "CMD_GET_INFO": b"0x01",  # 获取芯片信息
        "CMD_SEND_KB_GENERAL_DATA": b"0x02",  # 发送普通键盘数据
        "CMD_SEND_KB_MEDIA_DATA": b"0x03",  # 发送多媒体键盘数据
        "CMD_SEND_MS_ABS_DATA": b"0x04",  # 发送绝对鼠标数据
        "CMD_SEND_MS_REL_DATA": b"0x05",  # 发送相对鼠标数据
        "CMD_SEND_MY_HID_DATA": b"0x06",  # 发送自定义HID数据
        "CMD_READ_MY_HID_DATA": b"0x07",  # 读取自定义HID数据
        "CMD_GET_PARA_CFG": b"0x08",  # 获取参数设置
        "CMD_SET_PARA_CFG": b"0x09",  # 设置参数
        "CMD_GET_USB_STRING": b"0x0A",  # 获取字符串描述符
        "CMD_SET_USB_STRING": b"0x0B",  # 设置字符串描述符
        "MD_SET_DEFAULT_CFG": b"0x0C",  # 恢复出厂设置
        "CMD_RESET": b"0x0F"  # 复位芯片
    }

    """状态码表"""
    __statusCode = {
        b"00":"命令执行成功",
        b"E1":"串口接收一个字节超时",
        b"E2":"串口接收包头字节出错",
        b"E3":"串口接收命令码错误",
        b"E4":"累加和检验值不匹配",
        b"E5":"参数错误",
        b"E6":"帧正常，执行失败",
    }

    """键盘码映射表"""
    __keyBoardCode = {
        "stringMode": {
            "controlKeys": {
                "Backspace": 0x2A,
                "Tab": 0x2B,
                "ESC": 0x29,
                "Escape": 0x29,
                "CapsLock": 0x39,
                "Enter_L": 0x28,
                "Enter_R": 0x58,
                "Enter": 0x28,
                "Shift_L": 0xE1,
                "Shift_R": 0xE5,
                "Shift": 0xE1,
                "Ctrl_L": 0xE0,
                "Ctrl_R": 0xE4,
                "Ctrl": 0xE0,
                "Alt_L": 0xE2,
                "Alt_R": 0xE6,
                "Alt": 0xE2,
                "Insert": 0x49,
                "Delete": 0x4C,
                "Home": 0x4A,
                "End": 0x4D,
                "ArrowUp": 0x52,
                "ArrowDown": 0x51,
                "ArrowLeft": 0x50,
                "ArrowRight": 0x4F,
                "PgUp": 0x4B,
                "PgDn": 0x4E,
                "NumLock": 0x53,
                "PrintScreen": 0x46,
                "ScrollLock": 0x47,
                "Pause": 0x48,
                "Win_L": 0xE3,
                "MetaLeft": 0xE3,
                "Win_R": 0xE7,
                "MetaRight": 0xE7,
                "SpaceBar":0x2c,
                " ":0x2c
            },

            "cursorControlKeys": {
                "F1": 0x3A,
                "F2": 0x3B,
                "F3": 0x3C,
                "F4": 0x3D,
                "F5": 0x3E,
                "F6": 0x3F,
                "F7": 0x40,
                "F8": 0x41,
                "F9": 0x42,
                "F10": 0x43,
                "F11": 0x44,
                "F12": 0x45,
            },

            "numericKeypad": {
                "numpad_+": 0x57,
                "numpad_-": 0x56,
                "numpad_.": 0x63,
                "numpad_3": 0x5B,
                "numpad_6": 0x5E,
                "numpad_9": 0x61,
                "numpad_*": 0x55,
                "numpad_0": 0x62,
                "numpad_2": 0x5A,
                "numpad_5": 0x5D,
                "numpad_8": 0x60,
                "numpad_/": 0x54,
                "numpad_1": 0x59,
                "numpad_4": 0x5C,
                "numpad_7": 0x5F,
            },

            "characterKeys": {
                "`": 0x35,
                "~": 0x35,
                "!": 0x1E,
                "1": 0x1E,
                "@": 0x1F,
                "2": 0x1F,
                "#": 0x20,
                "3": 0x20,
                "$": 0x21,
                "4": 0x21,
                "%": 0x22,
                "5": 0x22,
                "^": 0x23,
                "6": 0x23,
                "&": 0x24,
                "7": 0x24,
                "*": 0x25,
                "8": 0x25,
                "(": 0x26,
                "9": 0x26,
                ")": 0x27,
                "0": 0x27,
                "_": 0x2D,
                "-": 0x2D,
                "+": 0x2E,
                "=": 0x2E,
                "q": 0x14,
                "w": 0x1A,
                "e": 0x08,
                "r": 0x15,
                "t": 0x17,
                "y": 0x1C,
                "u": 0x18,
                "i": 0x0C,
                "o": 0x12,
                "p": 0x13,
                "{": 0x2F,
                "[": 0x2F,
                "}": 0x30,
                "]": 0x30,
                "a": 0x04,
                "s": 0x16,
                "d": 0x07,
                "f": 0x09,
                "g": 0x0A,
                "h": 0x0B,
                "j": 0x0D,
                "k": 0x0E,
                "l": 0x0F,
                ";": 0x33,
                ":": 0x33,
                "'": 0x34,
                '"': 0x34,
                "z": 0x1D,
                "x": 0x1B,
                "c": 0x06,
                "v": 0x19,
                "b": 0x05,
                "n": 0x11,
                "m": 0x10,
                "<": 0x36,
                ",": 0x36,
                ">": 0x37,
                ".": 0x37,
                "?": 0x38,
                "/": 0x38,
                "|": 0x31,
                "\\": 0x31
            },
            
        },

        "ASCII_Code": {
            "65": 0x04,  # A
            "66": 0x05,  # B
            "67": 0x06,  # C
            "68": 0x07,  # D
            "69": 0x08,  # E
            "70": 0x09,  # F
            "71": 0x0A,  # G
            "72": 0x0B,  # H
            "73": 0x0C,  # I
            "74": 0x0D,  # J
            "75": 0x0E,  # K
            "76": 0x0F,  # L
            "77": 0x10,  # M
            "78": 0x11,  # N
            "79": 0x12,  # O
            "80": 0x13,  # P
            "81": 0x14,  # Q
            "82": 0x15,  # R
            "83": 0x16,  # S
            "84": 0x17,  # T
            "85": 0x18,  # U
            "86": 0x19,  # V
            "87": 0x1A,  # W
            "88": 0x1B,  # X
            "89": 0x1C,  # Y
            "90": 0x1D,  # Z
            "48": 0x27,  # 0
            "49": 0x1E,  # 1
            "50": 0x1F,  # 2
            "51": 0x20,  # 3
            "52": 0x21,  # 4
            "53": 0x22,  # 5
            "54": 0x23,  # 6
            "55": 0x24,  # 7
            "56": 0x25,  # 8
            "57": 0x26,  # 9
            "96": 0x62,  # 0 (小键盘)
            "97": 0x59,  # 1 (小键盘)
            "98": 0x5A,  # 2 (小键盘)
            "99": 0x5B,  # 3 (小键盘)
            "100": 0x5C,  # 4 (小键盘)
            "101": 0x5D,  # 5 (小键盘)
            "102": 0x5E,  # 6 (小键盘)
            "103": 0x5F,  # 7 (小键盘)
            "104": 0x60,  # 8 (小键盘)
            "105": 0x61,  # 9 (小键盘)
            "106": 0x55,  # * (小键盘)
            "107": 0x57,  # + (小键盘)
            "108": 0x58,  # Enter (小键盘)
            "109": 0x56,  # - (小键盘)
            "110": 0x63,  # . (小键盘)
            "111": 0x54,  # / (小键盘)
            "112": 0x3A,  # F1
            "113": 0x3B,  # F2
            "114": 0x3C,  # F3
            "115": 0x3D,  # F4
            "116": 0x3E,  # F5
            "117": 0x3F,  # F6
            "118": 0x40,  # F7
            "119": 0x41,  # F8
            "120": 0x42,  # F9
            "121": 0x43,  # F10
            "122": 0x44,  # F11
            "123": 0x45,  # F12
            "8": 0x2A,  # BackSpace
            "9": 0x2B,  # Tab
            # "12": 0x,  # Clear(未知)
            "13": 0x28,  # Enter
            "16": 0xE1,  # Shift
            "17": 0x2C,  # Control
            "18": 0xE2,  # Alt
            "20": 0x39,  # Cape Lock	
            "27": 0x29,  # Esc
            "32": 0x2c,  # Spacebar
            "33": 0x4B,  # Page Up	
            "34": 0x4E,  # Page Down
            "35": 0x4D,  # End
            "36": 0x4A,  # Home
            "37": 0x50,  # Left Arrow
            "38": 0x52,  # Up Arrow
            "39": 0x4F,  # Right Arrow
            "40": 0x51,  # Dw Arrow
            "45": 0x49,  # Insert
            "46": 0x4C,  # Delete
            "144": 0x53,  # Num Lock
            "186": 0x33,  # ;:
            "187": 0x2E,  # =+
            "188": 0x36,  # ,<
            "189": 0x2D,  # -_
            "190": 0x38,  # .>
            "191": 0x38,  # /?
            "192": 0x35,  # `~
            "219": 0x2F,  # [{
            "220": 0x31,  # /|
            "221": 0x30,  # ]}
            "222": 0x34,  # '"
        },

        "controlKeys": {
            "CTRL_L": 0x01,
            "SHIFT_L": 0x02,
            "ALT_L": 0x04,
            "WIN_L": 0x08,
            "CTRL_R": 0x10,
            "SHIFT_R": 0x20,
            "ALT_R": 0x40,
            "WIN_R": 0x80
        }
    }

    __serial = None

    __sendSerialCommandQueue = None

    def __init__(self, serial_post) -> None:
        self.__serial = serial.Serial(serial_post,9600)
        if not self.__serial.isOpen():
            Log.exception("串口打开失败")
            raise "串口打开失败"
        self.__sendSerialCommandQueue = Queue()
        Thread(target=self.__runQueueCommand,args=(),name="runQueueCommand").start()

    def __sendCMD(self,CMD_CODE:str,DATA_LIST:list = []):
        """发送串口命令

        Args:
            CMD_CODE (str): 命令码
            DATA_LIST (list, optional): 数据列表，可为空
        """

        HEAD = ["0x57","0xAB"]  # 命令头
        ADDR = "0x00"  # 命令地址
        LEN = len(DATA_LIST)  # 数据长度
        DATA = []  # 数据
        SUM = 0
        DATA+=HEAD
        DATA.append(ADDR)
        DATA.append(CMD_CODE)
        DATA.append(f"0x{LEN:02x}")
        DATA+=DATA_LIST
        for item in DATA:
                SUM += int(item,16)
        # print(SUM)
        # print()
        DATA.append(f"0x{int(bin(SUM)[-8:],2):02x}")
        Log.debug("Send Serial Command:"+str(DATA))
        for i in range(0,len(DATA)):
            DATA[i] = int(DATA[i],16)

        self.__serial.write(DATA)

    def __runQueueCommand(self):
        while not manage.stop:
            if self.__sendSerialCommandQueue.not_empty:
                Task = self.__sendSerialCommandQueue.get()
                self.__sendCMD(Task[0],Task[1])
        else:
            Log.success("HID队列任务进程已结束")
            return True

    def __addToCommandQueue(self,CMD_CODE:str,DATA_LIST:list = []):
        self.__sendSerialCommandQueue.put([CMD_CODE, DATA_LIST])

    def __getSerialOutput(self)->list:
        """获取串口输出

        Args:
            Serial: 串口

        Returns:
            串口输出16进制数组
        """
        i = 0
        while True:
            data = self.__serial.read_all()
            if data:
                hex_array = binascii.hexlify(data)
                hex_array = [hex_array[i:i+2] for i in range(0, len(hex_array), 2)][5:-1]
                Log.debug(f"Serial Output:{hex_array}")
                return hex_array
            time.sleep(0.1)
            i+=1
            if i > 20:
                Log.exception("获取串口输出超时")
                raise "获取串口输出超时"

            
    def __getHighByte(self,hexStr)->str:
        """工具-获取15进制高位比特（2位）

        Args:
            hexStr (_type_): 输入的16进制字符串

        Returns:
            str: 输出16进制字符串
        """
        high_byte = str(int(hexStr) >> 8)
        Log.debug(f"{hexStr} High Bete: 0x{int(high_byte):02X}")
        return f"0x{int(high_byte):02X}"

    def __getLowByte(self,hexStr)->str:
        """工具-获取15进制低位比特（2位）

        Args:
            hexStr (_type_): 输入的16进制字符串

        Returns:
            str: 输出16进制字符串
        """
        low_byte = str(int(hexStr) & 0xFF)
        Log.debug(f"{hexStr} Low Byte: 0x{int(low_byte):02X}")
        return f"0x{int(low_byte):02X}"

    def getInfo(self): 
        """获取基础信息

        Returns:
            Version: 芯片版本
            USB_Link: USB状态
            NUM_LOCK: 小键盘是否开启
            CAPS_LOOK: 大写锁定
            SCROLL_LOOK: 覆盖模式
        """
        self.__addToCommandQueue(self.__commandCode.get("CMD_GET_INFO"))
        res = self.__getSerialOutput(self.__serial)
        info = {
            "Version": f"1.{int(res[0],16)-47}",
            "USB_Link": bool(int(res[1],16)),
            "NUM_LOCK": bool(int(res[2],16)),
            "CAPS_LOOK": bool(int(res[3],16)),
            "SCROLL_LOOK": bool(int(res[4],16))
        }
        # print(info)
        return info

    def reset(self):
        """重置芯片

        Returns:
            命令返回码
        """
        self.__addToCommandQueue(self.__commandCode.get("CMD_RESET"))
        res = self.__getSerialOutput(self.__serial)[0]
        Log.info(self.__statusCode.get(res))
        return res

    def setDefaultConfig(self):
        """还原默认设置

        Returns:
            命令返回码
        """
        self.__addToCommandQueue(self.__commandCode.get("CMD_SET_DEFAULT_CFG"))
        res = self.__getSerialOutput(self.__serial)[0]
        Log.info(self.__statusCode.get(res))
        return res

    @Log.catch
    def clickMouseButton(self, button="left"):
        """点击鼠标

        Args:
            button (str, optional): 按下的键，默认左键，可选：left|right|center|freed
        """
        if button == "left":
            self.__addToCommandQueue(self.__commandCode.get("CMD_SEND_MS_ABS_DATA"),["0x02","0x01","0x00","0x00","0x00","0x00","0x00"])
        elif button == "right":
            self.__addToCommandQueue(self.__commandCode.get("CMD_SEND_MS_ABS_DATA"),["0x02","0x02","0x00","0x00","0x00","0x00","0x00"])   
        elif button == "center":
            self.__addToCommandQueue(self.__commandCode.get("CMD_SEND_MS_ABS_DATA"),["0x02","0x04","0x00","0x00","0x00","0x00","0x00"])
        elif button == "freed":
            self.__addToCommandQueue(self.__commandCode.get("CMD_SEND_MS_ABS_DATA"),["0x02","0x00","0x00","0x00","0x00","0x00","0x00"])
        else:
            raise "参数错误，可用参数：left、right、center、freed"

    @Log.catch
    def moveMouse(self,x_move,y_move,x_max=1920,y_max=1080,mode="absolute"):
        """移动鼠标

        Args:
            x_move (_type_): 要移动到的x坐标
            y_move (_type_): 要移动到的y坐标
            x_max (int, optional): x轴最大值，请填写屏幕分辨率
            y_max (int, optional): y轴最大值，请填写屏幕分辨率
            mode (str, optional): 模式选择，目前仅实现了absolute
        """
        if mode == "absolute":
            x_cur = int((4096 * x_move) / x_max)
            y_cur = int((4096 * y_move) / y_max)
            data = [
                "0x02",
                "0x00",
                self.__getLowByte(x_cur),
                self.__getHighByte(x_cur),
                self.__getLowByte(y_cur),
                self.__getHighByte(y_cur),
                "0x00"
            ]
            # print("data:"+data)
            self.__addToCommandQueue(self.__commandCode.get("CMD_SEND_MS_ABS_DATA"), data)
        elif mode == "relative":
            raise "相对移动尚未实现"

    @Log.catch
    def Mouse(self,x_move,y_move,button=None,distance=None,direction=None,x_max=1920,y_max=1080,mode="absolute"):
        """鼠标操作

        Args:
            x_move (_type_): 要移动到的x坐标
            y_move (_type_): 要移动到的y坐标
            button: 按下的键
            distance: 滚动齿数
            direction: 滚动方向
            x_max (int, optional): x轴最大值，请填写屏幕分辨率
            y_max (int, optional): y轴最大值，请填写屏幕分辨率
            mode (str, optional): 模式选择，目前仅实现了absolute
        """
        # 绝对定位
        if mode == "absolute":
            # 鼠标移动
            x_cur = int((4096 * x_move) / x_max)
            y_cur = int((4096 * y_move) / y_max)

            # 按键
            btn_cmd = "0x00"
            if button == 0:
                btn_cmd = "0x01"
            elif button == 2:
                btn_cmd = "0x02" 
            elif button == 1:
                btn_cmd = "0x04"
            elif button == None:
                pass
            else:
                raise "参数错误，可用参数：0(left)、2(right)、1(center)、None(down)"
            
            # 滚动
            if direction is not None:
                if 0 > distance > 126:
                    raise "滚动距离过长"
                if direction == "upper":
                    distance = "0x"+hex(distance+1)[2:].zfill(2)
                elif direction == "down":
                    distance = "0x"+hex(255-distance)[2:].zfill(2)
                else:
                    raise "参数错误，可用参数：upper、down"
            else:
                distance = "0x00"
            
            # 发送数据
            data = [
                "0x02",
                btn_cmd,
                self.__getLowByte(x_cur),
                self.__getHighByte(x_cur),
                self.__getLowByte(y_cur),
                self.__getHighByte(y_cur),
                distance
            ]
            self.__addToCommandQueue(self.__commandCode.get("CMD_SEND_MS_ABS_DATA"), data)
        # 相对定位
        elif mode == "relative":
            raise "相对移动尚未实现"

    @Log.catch 
    def scrollMouse(self,distance:int,direction="upper"):
        """滚动鼠标

        Args:
            distance (int): 滚动距离
            direction (str, optional): 滚动方向，可选值：upper、down
        """
        if 0 > distance > 126:
            raise "距离过长"
        if direction == "upper":
            distance = hex(distance+1)
            self.__addToCommandQueue(self.__commandCode.get("CMD_SEND_MS_ABS_DATA"),["0x02","0x00","0x00","0x00","0x00","0x00",distance])
        elif direction == "down":
            distance = hex(255-distance)
            self.__addToCommandQueue(self.__commandCode.get("CMD_SEND_MS_ABS_DATA"),["0x02","0x00","0x00","0x00","0x00","0x00",distance])
        else:
            raise "参数错误，可用参数：upper、down"

    @Log.catch
    def keyBoardInput(self,key = None,mode="String_Mode",controlKeys = [],holdDown=False):
        """键盘输入

        Args:
            key (_type_): 键，如需按下多个键请传入列表，最大6个
            mode (_type_): 模式，可选String_Mode、ASCII_Mode、Clear
            controlKeys (list): 控制键，最大8个
            holdDown (bool, optional): 是否按住，默认False
        """
        
        if mode not in ["String_Mode", "ASCII_Mode", "Clear"] and not key:
            raise "非Clear Mode请输入参数"
        if isinstance(key,list):
            if not 0 < len(key) <= 6:
                raise "当输入为列表时仅允许1-6个键"
        data = []
        if controlKeys:
            if isinstance(controlKeys,list):
                temp = 0
                for Ckey in controlKeys:
                    temp += self.__keyBoardCode["controlKeys"].get(Ckey)
                data.append(hex(temp))
            else:
                data.append(hex(self.__keyBoardCode["controlKeys"].get(controlKeys)))
        else:
            data.append("0x00")
        data.append("0x00")

        if mode == "String_Mode":
            if isinstance(key,list):
                for item in key:
                    for area_list in self.__keyBoardCode["stringMode"].values():
                        temp = False
                        for index,kb_code in area_list.items():     
                            if index == item:
                                hex_data = f"0x{int(kb_code):02X}"
                                Log.debug(hex_data)
                                data.append(hex_data)
                                temp = True
                                break
                        if temp:
                            break
            else:
                for area_list in self.__keyBoardCode["stringMode"].values():
                    temp = False
                    for index,kb_code in area_list.items():     
                        if index == key:
                            hex_data = f"0x{int(kb_code):02X}"
                            Log.debug(hex_data)
                            data.append(hex_data)
                            temp = True
                            break
                    if temp:
                        break
            # return data
        elif mode == "ASCII_Mode":
            if isinstance(key,list):
                for item in key:
                    data.append(self.__keyBoardCode["ASCII_Code"].get(item))
            else:
                data.append(self.__keyBoardCode["ASCII_Code"].get(key))
        elif mode == "Clear":
            self.__addToCommandQueue(self.__commandCode.get("CMD_SEND_KB_GENERAL_DATA"),["0x00","0x00","0x00","0x00","0x00","0x00","0x00","0x00"])
            return
        else:
            raise "未知的模式，可选值：String_Mode、ASCII_Mode、Clear"

        for i in range(0,8-len(data)):
            data.append("0x00")
        self.__addToCommandQueue(self.__commandCode.get("CMD_SEND_KB_GENERAL_DATA"),data)
        if not holdDown:
            self.__addToCommandQueue(self.__commandCode.get("CMD_SEND_KB_GENERAL_DATA"), [
                                     "0x00", "0x00", "0x00", "0x00", "0x00", "0x00", "0x00", "0x00"])

    def inputString(self,str:str):
        """快速输入字符串

        Args:
            str (str): 字符串
        """
        Log.info(f"input String: {str}")
        for char in str:
            if char == "\n":
                self.keyBoardInput("Enter_L")
            elif char == "\t" or char == "  ":
                self.keyBoardInput("Tab")
            elif char == " ":
                self.keyBoardInput("SpaceBar")
            elif char.isupper() or char in ["~","!","@","#","$","%","^","&","*","(",")","_","+","{","}","|",":",'"',"<",">","?"]:
                self.keyBoardInput(char.lower(),controlKeys=["SHIFT_L"])
            elif not char.isupper():
                self.keyBoardInput(char,"String_Mode")


if __name__ == "__main__":
    HID = ch3929("/dev/ttyS5")
    HID.inputString("hello world")