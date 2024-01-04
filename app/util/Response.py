import json
from django.shortcuts import HttpResponse
from datetime import date, datetime


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)

def ResponseJson(data: dict):
    return HttpResponse(json.dumps(data, cls=ComplexEncoder), content_type="application/json")
