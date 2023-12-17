from typing import Optional
from rest_framework.response import Response


class CustomResponse(Response):

    def __init__(self, data=None, status=None, has_error: Optional[bool | None] = None, headers=None, errors=None, content_type=None):
        data = {"hasError": has_error, "errors": errors, "resultObject": data}
        super().__init__(data, status, headers, exception=has_error, content_type=content_type)
