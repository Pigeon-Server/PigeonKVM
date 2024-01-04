try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

from app.util.logger import Log

try:
    with open("configs/config.toml", "rb") as f:
        main_config = tomllib.load(f)
        Log.success("配置文件加载完成")
except Exception:
    raise RuntimeError("配置文件加载失败")