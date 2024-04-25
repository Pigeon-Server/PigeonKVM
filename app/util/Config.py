import json

import app.apps as apps
from app.models import Settings
from app.entity.Config import config as configObj

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

from app.util.logger import Log


# 加载配置文件到对象
def loadConfig(config):
    settings = Settings.objects.all()
    for item in settings:
        settingKeySplit = item.Settings.split('.')
        if hasattr(config, settingKeySplit[0]):
            config_obj = getattr(config, settingKeySplit[0])
            settingKeys = settingKeySplit[-1:]
            annotations = config_obj.__annotations__
            for index, split in enumerate(settingKeys):
                if index == len(settingKeys) - 1:
                    setattr(config_obj, split, annotations.get(split)(item.value))
                elif hasattr(config_obj, split):
                    config_obj = getattr(config_obj, split)
    return config


# 保存对象到数据库中
def saveConfig(obj):
    for item1Key, item1Value in obj.__dict__.items():
        temp = item1Key + "."
        for item2Key, item2Value in item1Value.__dict__.items():
            temp += item2Key
            settings = Settings.objects.filter(Settings=temp).first()
            if settings:
                settings.value = str(item2Value)
                settings.save()
            else:
                Settings.objects.create(Settings=temp, value=str(item2Value))
            temp = item1Key + "."
    return loadConfig(obj)


# 将字典转换到对象
def dictToConfig(data, obj):
    """
    :param data: 数据字典
    :param obj: 对象模板
    :return: 带数据的对象
    """
    temp_config = obj()
    for key1 in data.keys():
        if hasattr(temp_config, key1):
            temp = getattr(temp_config, key1)
            item = data.get(key1)
            annotations = temp.__annotations__
            for key2 in item.keys():
                if hasattr(temp, key2):
                    setattr(temp, key2, annotations.get(key2)(item.get(key2)))
        else:
            continue
    return temp_config


try:
    with open("configs/config.toml", "rb") as f:
        main_config = tomllib.load(f)
        Log.success("基本配置文件加载完成")
except Exception as err:
    raise RuntimeError("基本配置文件加载失败，应用启动失败")

# if apps.STARTAPP:
#     config = configObj()
#     config = loadConfig(config)
