from app.util.logger import Log
from app.models import Users, Permission_groups, Audit, System_Log, Access_Log, FileChange_Log


# 获取最大页数
@Log.catch
def getMaxPage(count: int, size: int) -> int:
    """
    :param count: 总条数
    :param size: 页大小
    :return: 共x页
    """
    return (count + size - 1) // size


# 获取指定页内容
@Log.catch
def getPageContent(model, page: int, size: int):
    """
    :param model: Model实体
    :param page: 页码
    :param size: 页大小
    :return:
    """
    if getMaxPage(model.count(), size) >= page:
        pageStart = size * (page - 1)
        pageEnd = pageStart + size
        return model.values()[pageStart:pageEnd]
    else:
        return model.values()[model.count() - size if not model.count() - size < 0 else 0:model.count()]


# 写访问日志
@Log.catch
def writeAccessLog(user_id, ip: str, module: str):
    """
    :param user_id: 用户id
    :param ip: 用户IP地址
    :param module: 模块
    :return:
    """
    Access_Log.objects.create(user=Users.objects.filter(id=user_id).first(), ip=ip, module=module)


# 写系统日志
@Log.catch
def writeSystemLog(level: int, module: str, content: str):
    """
    :param level: 日志等级
    :param module: 模块
    :param content: 内容
    :return:
    """
    System_Log.objects.create(level=level, module=module, content=content)


# 写审计内容
@Log.catch
def writeAudit(user_id: int, action: str, module: str, content: str):
    """
    :param user_id: 用户ID
    :param action: 动作
    :param module: 模块
    :param content: 内容
    """
    Audit.objects.create(user=Users.objects.filter(id=user_id).first(), action=action, module=module, content=content)


# 写文件记录
@Log.catch
def writeFileChangeLog(user_id: int, action: str, filepath: str):
    """
    :param user_id: 用户ID
    :param action: 动作
    :param filepath: 目标
    """
    FileChange_Log.objects.create(user=Users.objects.filter(id=user_id).first(), action=action, filepath=filepath)



