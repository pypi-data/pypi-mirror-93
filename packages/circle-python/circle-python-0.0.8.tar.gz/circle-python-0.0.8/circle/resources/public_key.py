from circle.resources.abstract import (
    ListableAPIResource,
    RetrievableAPIResource
)


class PublicKey(ListableAPIResource):
    """
    https://developers.circle.com/reference/encryption
    """

    OBJECT_NAME = "encryption.public"  # The object name as it maps to the API resource.
