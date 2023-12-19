from rest_framework.renderers import JSONRenderer


class CustomRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        res_data = {"hasError": None, "errors": None, "resultObject": None}
        status_code = renderer_context.get("response").status_code

        if str(status_code).startswith('2'):
            res_data["hasError"] = False
            res_data["resultObject"] = data
        else:
            res_data["hasError"] = True
            res_data["errors"] = data

        return super().render(res_data, accepted_media_type, renderer_context)
