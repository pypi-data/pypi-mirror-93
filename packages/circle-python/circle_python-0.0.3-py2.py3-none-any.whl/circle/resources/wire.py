from circle.resources.abstract import CreateableAPIResource
from circle.resources.abstract import RetrievableAPIResource


class Wire(CreateableAPIResource, RetrievableAPIResource):

    OBJECT_NAME = "banks.wires"
