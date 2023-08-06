from circle.resources.abstract import CreateableAPIResource
from circle.resources.abstract import RetrievableAPIResource


class Ach(CreateableAPIResource, RetrievableAPIResource):

    OBJECT_NAME = "banks.ach"
