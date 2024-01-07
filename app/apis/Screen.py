from django.http import StreamingHttpResponse, HttpResponse

import app.apps
from app.util.DataBaseTools import writeAudit


def getScreen(req):
    frame = app.apps.cameraObj.getDisplayFrame()
    # print(frame)
    writeAudit(req.session.get("userId"), "Get Display Screen Image", "control", "")
    return HttpResponse(content=frame, content_type="image/jpeg")
