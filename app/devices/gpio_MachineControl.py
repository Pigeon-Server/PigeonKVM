try:
    import wiringpi
    from wiringpi import GPIO
except:
    import gpio as GPIO

class MachineControl:
    class ControlMode:
        wPi = 0  # 香橙派的GPIO控制器
        GPIO_ID = 1  # 通用GPIO控制器

    class GpioMode:
        IN = 0
        OUT = 1

    __Power_LED: int = 9
    __HDD_LED: int = 8
    __Power_Btn: int = 6
    __Restart_Btn: int = 5
    __UsbDisk_EN: int = 18
    __UsbDisk_Switch: int = 17
    __GPIO_ControlMode: ControlMode = ControlMode.wPi

    def __init__(self, GPIO_ControlMode: ControlMode, Power_LED: int, HDD_LED: int, Power_Btn: int, Restart_Btn: int, UsbDisk_EN: int, UsbDisk_Switch: int):
        """
        :param GPIO_ControlMode: GPIO控制模式
        :param Power_LED: 电源指示灯GPIO编号
        :param HDD_LED: 硬盘指示灯GPIO编号
        :param Power_Btn: 电源按键GPIO编号
        :param Restart_Btn: 重启按键GPIO编号
        :param UsbDisk_EN: 使能USB切换器GPIO编号
        :param UsbDisk_Switch: USB切换信号
        """
        self.__GPIO_ControlMode = GPIO_ControlMode
        self.__Power_LED = Power_LED
        self.__HDD_LED = HDD_LED
        self.__Power_Btn = Power_Btn
        self.__Restart_Btn = Restart_Btn
        self.__UsbDisk_EN = UsbDisk_EN
        self.__UsbDisk_Switch = UsbDisk_Switch

        if self.__GPIO_ControlMode == self.ControlMode.wPi:
            import wiringpi
            from wiringpi import GPIO
        elif self.__GPIO_ControlMode == self.ControlMode.GPIO_ID:
            import gpio as GPIO
        self.__initGpio()

    # GPIO模式设置
    def setGpioMode(self, mode: GpioMode, default: bool):
        """
        :param mode: GPIO模式
        :param default: 默认值
        :return:
        """
        if self.__GPIO_ControlMode == self.ControlMode.wPi:
            pass
        elif self.__GPIO_ControlMode == self.ControlMode.GPIO_ID:
            pass

    def __setGpioValue(self, pin: int, value: bool):
        if self.__GPIO_ControlMode == self.ControlMode.wPi:
            pass
        elif self.__GPIO_ControlMode == self.ControlMode.GPIO_ID:
            if GPIO.mode(pin) == GPIO.OUT:
                return GPIO.write(pin, value)
            else:
                raise RuntimeError("GPIO value is not writable")

    def __getGpioValue(self, pin: int):
        if self.__GPIO_ControlMode == self.ControlMode.wPi:
            pass
        elif self.__GPIO_ControlMode == self.ControlMode.GPIO_ID:
            if GPIO.mode(pin) == GPIO.IN:
                return GPIO.read(pin)
            else:
                raise RuntimeError("GPIO value is not readable")


    # 初始化GPIO
    def __initGpio(self):
        if self.__GPIO_ControlMode == self.ControlMode.wPi:
            # Power_LED
            wiringpi.pinMode(self.__Power_LED, GPIO.INPUT);
            # HDD_LED
            wiringpi.pinMode(self.__HDD_LED, GPIO.INPUT);
            # Power_Btn
            wiringpi.pinMode(self.__Power_Btn, GPIO.INPUT);
            # Restart_Btn
            wiringpi.pinMode(self.__Restart_Btn, GPIO.INPUT);
            # UsbDisk_EN
            wiringpi.pinMode(self.__UsbDisk_EN, GPIO.OUTUP);
            # UsbDisk_Switch
            wiringpi.pinMode(self.__UsbDisk_Switch, GPIO.OUTUP);
        elif self.GPIO_ControlMode == self.ControlMode.GPIO_ID:
            # Power_LED
            GPIO.setup(self.__Power_LED, GPIO.IN)
            # HDD_LED
            GPIO.setup(self.__HDD_LED, GPIO.IN)
            # Power_Btn
            GPIO.setup(self.__Power_Btn, GPIO.OUT)
            # Restart_Btn
            GPIO.setup(self.__Restart_Btn, GPIO.OUT)
            # UsbDisk_EN
            GPIO.setup(self.__UsbDisk_EN, GPIO.OUT)
            GPIO.output(self.__UsbDisk_EN, GPIO.LOW)
            # UsbDisk_Switch
            GPIO.setup(self.__UsbDisk_Switch, GPIO.OUT)
            GPIO.output(self.__UsbDisk_Switch, GPIO.HIGH)

    # 获取电源指示灯状态
    def getPowerLedStatus(self):
        pass

    # 获取硬盘指示灯状态
    def getHddLedStatus(self):
        pass

    # 点击电源键
    def clickPowerButton(self):
        pass

    # 点击重启键
    def clickRestartButton(self):
        pass