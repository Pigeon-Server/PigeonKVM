from django.apps import AppConfig
from control.util.ch9329 import ch3929
from control.util.camera import camera
from util.logger import Log


class ControlConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'control'
    __HID_Device = None
    __Camera_Device = None

    def __init__(self, *args, **kwargs):
        super(ControlConfig, self).__init__(*args, **kwargs)
        Log.info("Control: Initializing start")

    def ready(self):
        # self.__HID_DEVICE = ch3929()
        self.__Camera_Device = camera()
        Log.success("Control: Initialization complete")

    def get_device(self):
        return self.__HID_Device

    def get_camera(self):
        return self.__Camera_Device
