from circle.resources.abstract import RetrievableAPIResource
from circle.resources.abstract import ListableAPIResource
from circle.resources.abstract import CreateableAPIResource


class Transfer(CreateableAPIResource, ListableAPIResource):
    """
    https://developers.circle.com/reference#payouts-transfers-create
    """

    OBJECT_NAME = "transfers"  # The object name as it maps to the API resource.
