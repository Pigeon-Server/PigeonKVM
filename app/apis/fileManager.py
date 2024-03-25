import aiofiles
from asgiref.sync import sync_to_async
from django.http import HttpResponse, StreamingHttpResponse, HttpResponseNotFound, HttpResponseForbidden, \
    HttpResponseServerError
from django.shortcuts import redirect

from app.models import Temporary_link
import os

from app.util.DataBaseTools import writeFileChangeLog


async def temporary_link_download(request, token):
    async def file_iterator(file, chunk_size):
        async with aiofiles.open(file, 'rb') as f:
            while True:
                chunk = await f.read(chunk_size)
                if not chunk:
                    break
                yield chunk

    userID = request.session.get("userID")
    TL_Model = await sync_to_async(Temporary_link.objects.filter)(userID=userID, token=token)
    TL_Model = await sync_to_async(TL_Model.first)()

    if TL_Model:
        if not TL_Model.used:
            filePath = TL_Model.filePath
            basename = os.path.basename(filePath)
            TL_Model.used = True
            await sync_to_async(TL_Model.save)()
            await sync_to_async(writeFileChangeLog)(request.session.get("userID"), "Download File", filePath)

            try:
                response = StreamingHttpResponse(file_iterator(filePath, chunk_size=8192), content_type='application/octet-stream')
                response['Content-Disposition'] = f'attachment; filename="{basename}"'
                return response
            except Exception:
                return redirect(f"/error?errorCode=500&errorMessage=文件{basename}读取失败")
        else:
            return redirect("/error?errorCode=403&errorMessage=文件已超过允许下载次数")
    else:
        return redirect("/error?errorCode=404&errorMessage=临时文件不存在")
