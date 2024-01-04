from django.http import HttpResponse, FileResponse, StreamingHttpResponse
from app.models import Temporary_link
import os

from app.util.DataBaseTools import writeFileChangeLog


def temporary_link_download(request, token):
    userID = request.session.get("userID")
    TL_Model = Temporary_link.objects.filter(userID=userID, token=token).first()

    if TL_Model:
        if not TL_Model.used:
            filePath = TL_Model.filePath
            TL_Model.used = True
            TL_Model.save()
            writeFileChangeLog(request.session.get("userID"), "Download File", filePath)
            return FileResponse(open(filePath, "rb"))
        else:
            return HttpResponse("文件已超过允许下载次数")
    else:
        return HttpResponse("文件不存在或没有访问权限")
