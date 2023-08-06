from circle.resources.abstract.api_resource import APIResource
from circle.api_requestor import APIRequestor
from circle import util


class ListableAPIResource(APIResource):
    @classmethod
    def list(cls, api_key=None, **params):
        requestor = APIRequestor(api_key)
        url = cls.class_url()
        response, api_key = requestor.request("get", url, params)
        circle_object = util.convert_to_circle_object(response, api_key)
        # circle_object._retrieve_params = params
        return circle_object
