import json
from typing import Optional
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer


class CustomResponse(Response):

    def __init__(self, data=None, status=None, has_error: Optional[bool | None] = None, headers=None, errors=None, content_type=None):
        data = {"hasError": has_error, "errors": errors, "resultObject": data}
        super().__init__(data, status, headers, exception=has_error, content_type=content_type)


class CustomRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        res_data = {"hasError": None, "errors": None, "resultObject": None}
        print("Accepted Media Type:-", accepted_media_type)
        print("Renderer Context:-", renderer_context)
        status_code = renderer_context.get("response").status_code

        if str(status_code).startswith('2'):
            res_data["hasError"] = False
            res_data["resultObject"] = data
        else:
            res_data["hasError"] = True
            res_data["errors"] = data

        return super().render(res_data, accepted_media_type, renderer_context)
