from django.http import StreamingHttpResponse, HttpResponse

import app.apps


def getScreen(req):
    frame = app.apps.cameraObj.getDisplayFrame()
    # print(frame)
    return HttpResponse(content=frame, content_type="image/jpeg")
